# AI Rule: Simplifying Rust FFI Integration with External C/C++ Libraries

This document outlines best practices for integrating external C/C++ libraries into a Rust project using Foreign Function Interface (FFI), aiming for a clean, reproducible, and developer-friendly setup.

## 1. Build Script (`build.rs`) Best Practices

*   **Minimize Build Script Dependencies:**
    *   Primarily utilize the `cc` crate for compiling C/C++ source code.
    *   Use the `bindgen` crate for generating Rust bindings from C/C++ headers.
    *   **Avoid external build system dependencies** like `pkg-config`, `cmake`, or `autotools` directly within `build.rs` if possible. Relying on these can make the build process less portable and more dependent on the user's system environment.

*   **Vendoring C/C++ Source Code:**
    *   **Preferred Method:** Include the C/C++ source code directly within your Rust project's repository. This can be done by copying the source files or, more commonly, by using a **Git submodule** to track a specific version of the external library.
    *   **Benefits:**
        *   **Reproducible Builds:** Ensures that builds are consistent across different environments and over time, as they don't rely on system-installed versions of the library which might vary.
        *   **Simplified CI/CD:** Continuous integration pipelines don't need to install specific versions of C/C++ libraries.
        *   **Offline Builds:** Allows building the project without internet access to fetch library sources.

*   **Feature Flags for Build Flexibility:**
    *   **`vendored` Feature (Enabled by Default):**
        *   Implement a feature flag (e.g., named `vendored`) that, when enabled (which should be the default), instructs `build.rs` to compile the included (vendored) C/C++ source code using the `cc` crate.
        *   This allows users to potentially opt-out if they have a system-provided version they prefer to link against (though vendoring is generally safer for library crates).
    *   **`bindgen` Feature (Optional, for Development):**
        *   Implement a feature flag (e.g., `bindgen`) that, when enabled, triggers `bindgen` to regenerate the Rust FFI bindings from the C/C++ headers.
        *   **Default Behavior:** For users of your crate, include **pre-generated bindings** directly in your repository (e.g., `src/bindings.rs`). This is crucial because `bindgen` often requires `libclang` (part of LLVM/Clang) to be installed, which can be a heavy dependency and a barrier for users. The `bindgen` feature should primarily be for crate developers during updates to the C/C++ library.

*   **Platform-Specific Bindings & Conditional Compilation:**
    *   Recognize that some C/C++ libraries expose different APIs, type representations (e.g., `size_t`, `long`), or structures across different platforms (Windows, macOS, Linux, different architectures).
    *   If necessary, generate and include platform-specific bindings. Use conditional compilation attributes (`#[cfg(...)]`) in `build.rs` to select the correct C/C++ sources or compiler flags, and in your Rust code to use the appropriate bindings.
    *   `bindgen` can often handle many platform differences, but manual adjustments or separate binding files might be needed for complex cases.

## 2. `build.rs` Implementation Example

```rust
// build.rs

// This build script assumes the C/C++ sources are in a `c_src` directory
// and headers are appropriately referenced, potentially via a `wrapper.h`.

fn main() {
    // --- Compile C/C++ Sources (if 'vendored' feature is enabled) ---
    // By default, we assume 'vendored' is active or no feature flag controls this part,
    // meaning we always try to build the vendored code.
    // For more control, you could wrap this in `#[cfg(feature = "vendored")]`
    // and potentially add a way to link to a system library if 'vendored' is off.

    let mut build = cc::Build::new();
    build.file("c_src/foo.c")
         .file("c_src/bar.c")
         // Add include paths if your C code is structured in subdirectories
         // .include("c_src/include")
         // Add defines or other compiler flags as needed
         // .define("SOME_MACRO", "1")
         .warnings(true) // Enable warnings
         .compile("my_c_library"); // Output static library name (e.g., libmy_c_library.a)

    println!("cargo:rerun-if-changed=c_src/foo.c");
    println!("cargo:rerun-if-changed=c_src/bar.c");
    println!("cargo:rerun-if-changed=c_src/wrapper.h"); // Important for bindgen

    // --- Generate Bindings (if 'bindgen' feature is enabled) ---
    // This part is typically only run by developers of the crate, not end-users.
    // End-users will use the pre-generated `src/bindings.rs`.
    #[cfg(feature = "bindgen")]
    {
        generate_bindings();
    }
}

#[cfg(feature = "bindgen")]
fn generate_bindings() {
    use std::env;
    use std::path::PathBuf;

    // Tell cargo to invalidate the built crate whenever the wrapper changes
    println!("cargo:rerun-if-changed=c_src/wrapper.h");

    let bindings = bindgen::Builder::default()
        // The input header we would like to generate bindings for.
        .header("c_src/wrapper.h")
        // Tell cargo to invalidate the built crate whenever any of the
        // included header files changed.
        .parse_callbacks(Box::new(bindgen::CargoCallbacks::new()))
        // Customize bindgen options as needed:
        // .allowlist_function("cool_c_function")
        // .allowlist_type("CoolCType")
        // .blocklist_item("SOME_CONSTANT_WE_DONT_WANT")
        // .rustified_enum("MyCEnum")
        // Finish the builder and generate the bindings.
        .generate()
        // Unwrap the Result and panic on failure.
        .expect("Unable to generate bindings");

    // Write the bindings to the $OUT_DIR/bindings.rs file.
    // let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    // bindings
    //     .write_to_file(out_path.join("bindings.rs"))
    //     .expect("Couldn't write bindings!");
    //
    // OR, more commonly for pre-generating, write to src/bindings.rs
    // This requires manual step by crate dev: enable 'bindgen' feature, build, then commit bindings.rs.
    let crate_root = PathBuf::from(env::var("CARGO_MANIFEST_DIR").unwrap());
    bindings
        .write_to_file(crate_root.join("src").join("bindings.rs"))
        .expect("Couldn't write bindings to src/bindings.rs!");
    
    eprintln!("Successfully generated bindings to src/bindings.rs. Remember to commit this file.");
}

// In your lib.rs or main.rs, you would then include the bindings:
// ```rust
// #[allow(non_upper_case_globals)]
// #[allow(non_camel_case_types)]
// #[allow(non_snake_case)]
// #[allow(dead_code)]
// include!(concat!(env!("CARGO_MANIFEST_DIR"), "/src/bindings.rs"));
// // Or if writing to OUT_DIR:
// // include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
// ```
```

## 3. `wrapper.h` for `bindgen`

Create a `wrapper.h` file (e.g., in `c_src/wrapper.h`) that includes all the C/C++ headers for which you want to generate Rust bindings. This simplifies the `bindgen` setup.

```c
// c_src/wrapper.h
#include "foo.h" // Assuming foo.h contains declarations from foo.c
#include "bar.h" // Assuming bar.h contains declarations from bar.c
// Add other necessary headers here
```

## 4. Cargo.toml Configuration

```toml
[package]
name = "my-rust-ffi-crate"
version = "0.1.0"
edition = "2021"
build = "build.rs" # Specify the build script

[dependencies]
# Add other Rust dependencies here

[build-dependencies]
cc = "1.0"
# bindgen is optional for end-users if bindings are pre-generated
bindgen = { version = "0.69", optional = true }

[features]
default = ["vendored"]
vendored = [] # Enables building the vendored C/C++ code
bindgen = ["dep:bindgen"] # Enables regenerating bindings (for crate developers)
```

## Summary of Benefits:

*   **Reproducibility:** Vendoring source code ensures builds are consistent.
*   **Ease of Use:** Pre-generated bindings mean users of your crate don't need LLVM/Clang installed.
*   **Flexibility:** Feature flags allow developers to regenerate bindings or potentially link against system libraries if absolutely necessary (though vendoring is preferred for libraries).
*   **Clarity:** Centralizes C/C++ compilation and binding generation logic in `build.rs`.

By following these guidelines, Rust FFI integration becomes more manageable, robust, and user-friendly.
