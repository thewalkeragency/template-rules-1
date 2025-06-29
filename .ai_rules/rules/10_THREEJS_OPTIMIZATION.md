# AI Rule: Optimizing Three.js Development for Performance and Maintainability

This document outlines best practices for developing efficient, high-performing, and maintainable 3D web applications using Three.js. These rules apply whether using Three.js directly or via libraries like React Three Fiber (R3F). For R3F specific implementation, also refer to `.ai_rules/rules/03_FRONTEND.md`.

## 1. Geometry and Object Management

*   **Use `BufferGeometry`:**
    *   **Mandatory:** Prefer `BufferGeometry` over the legacy `Geometry` class for all new meshes. `BufferGeometry` is more performant and memory-efficient as it stores data directly in typed arrays suitable for direct GPU consumption.
*   **Merge Geometries:**
    *   When multiple meshes share the same material and are static, merge their geometries into a single `BufferGeometry` (e.g., using `BufferGeometryUtils.mergeBufferGeometries`). This significantly reduces the number of draw calls, a major performance bottleneck.
    *   Be mindful that merging makes individual manipulation of the original objects harder. Best for static scenery or collections of identical objects.
*   **Instanced Rendering (`InstancedMesh`):**
    *   For rendering a large number of identical (or near-identical) objects that may have different positions, rotations, or scales, use `InstancedMesh`. This allows rendering all instances in a single draw call.
*   **Implement Object Pooling:**
    *   For objects that are frequently created and destroyed (e.g., particles, projectiles), implement an object pooling system. Reuse objects from a pool instead of constantly allocating and deallocating memory, which can lead to garbage collection pauses and performance degradation.

## 2. Texture and Asset Optimization

*   **Compress Textures:**
    *   Utilize compressed texture formats appropriate for the web (e.g., JPEG for opaque images, PNG for transparency where needed, WebP for a good balance).
    *   For GPU-specific compression, consider formats like Basis Universal (KTX2/Basis) which can transcode to various native GPU formats, reducing GPU memory usage and improving loading times.
*   **Use Power-of-Two (POT) Textures:**
    *   Ensure texture dimensions are powers of two (e.g., 128x128, 256x256, 512x512, 1024x1024). While modern GPUs and WebGL2 handle Non-Power-of-Two (NPOT) textures better, POT textures can still offer performance benefits, especially for mipmapping and texture wrapping modes.
*   **Mipmapping:**
    *   Enable mipmapping for textures that are viewed at various distances. Mipmaps are pre-calculated, lower-resolution versions of a texture, which reduce aliasing artifacts and improve rendering performance for distant objects.
*   **Optimize Models (glTF/GLB):**
    *   Use the glTF/GLB format for 3D models, as it's designed for efficient transmission and loading on the web.
    *   Optimize models using tools like `gltf-pipeline` or Blender export settings to reduce vertex count, apply Draco mesh compression, and compress textures.

## 3. Rendering and Animation

*   **Use `requestAnimationFrame`:**
    *   **Mandatory:** Employ `requestAnimationFrame` for driving your rendering loop. This synchronizes rendering with the browser's refresh rate, leading to smoother animations and more efficient use of resources compared to `setTimeout` or `setInterval`.
*   **Implement Level of Detail (LOD):**
    *   For complex objects or scenes with many objects, use `THREE.LOD`. This allows you to display simpler versions of an object when it's far from the camera and more detailed versions when it's close, improving performance by reducing the polygon count for distant objects.
*   **Minimize Lights and Shadows:**
    *   Lights, especially those that cast shadows (`castShadow=true`), are computationally expensive.
    *   Limit the number of dynamic lights in your scene.
    *   Use baked lighting (lightmaps) for static scenes where possible.
    *   Optimize shadow map resolution (`shadow.mapSize`) and camera frustum (`shadow.camera`) to cover only necessary areas.
*   **Frustum Culling:**
    *   Three.js performs frustum culling by default (objects outside the camera's view are not rendered). Ensure your objects have correctly computed bounding spheres/boxes for this to work effectively.
*   **Conditional Rendering / Updates:**
    *   Only re-render the scene or update animations if something has actually changed. Avoid unnecessary rendering calls in a static scene.

## 4. Resource Management

*   **Dispose Unused Resources:**
    *   **Critical:** Properly dispose of Three.js objects (geometries, materials, textures, render targets) when they are no longer needed to prevent memory leaks. Call the `.dispose()` method on these objects and remove them from their parent.
    *   For R3F, this is often handled more automatically when components unmount, but be mindful with manually created Three.js objects.
*   **Monitor Performance:**
    *   Use tools like `Stats.js` or browser developer tools (Performance tab, GPU profiler) to track frame rate (FPS), memory usage, draw calls, and identify performance bottlenecks.
    *   The `three.js devtools` browser extension can also be very helpful for inspecting scenes.

## 5. Code Structure and Integration

*   **Use Build Tools/Bundlers:**
    *   Utilize modern JavaScript build tools like Webpack, Rollup, Vite, or Parcel to manage dependencies, bundle your code, and perform optimizations (e.g., tree-shaking, minification).
*   **Modular Code:**
    *   Organize your Three.js code into reusable modules or components, especially when using frameworks like React (R3F).
*   **Ensure Cross-Browser Compatibility:**
    *   Test your Three.js application across different browsers (Chrome, Firefox, Safari, Edge) and devices to ensure consistent performance and visual output. Be aware of varying WebGL capabilities or limitations.
*   **Lazy Loading:**
    *   Load assets (models, textures) on demand or asynchronously to improve initial page load time. Show loading indicators to the user.

By adhering to these best practices, you can create Three.js applications that are not only visually impressive but also performant, memory-efficient, and maintainable.
