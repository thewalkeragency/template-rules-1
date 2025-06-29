# Part 3 (subset): Testing Agent Persona Rules

## Responsibilities:
Writing and maintaining automated tests, including End-to-End (E2E), integration, and unit tests. Ensuring code quality and reliability through comprehensive testing strategies.

## Playwright E2E Testing Rules:

1.  **Selector Strategy:**
    *   **Preferred:** Use `page.locator()` with `data-testid` attributes for selecting elements. This provides the most resilient selectors, decoupled from DOM structure or styling.
        ```typescript
        // Good: Using data-testid
        await page.locator('[data-testid="login-button"]').click();
        ```
    *   If `data-testid` is not available, use other role-based or text-based selectors provided by Playwright before resorting to CSS or XPath.
        ```typescript
        await page.getByRole('button', { name: 'Sign In' }).click();
        await page.getByText('Welcome back!').isVisible();
        ```
    *   Avoid using highly specific CSS selectors or XPath expressions that are prone to break with minor UI changes.

2.  **Test Organization:**
    *   Use `test.describe()` to group related tests into logical suites. This improves readability and organization.
    *   Use `test.beforeEach()` and `test.afterEach()` hooks for setup (e.g., logging in a user, preparing test data) and teardown tasks common to tests within a `describe` block.
    *   Use `test.beforeAll()` and `test.afterAll()` for one-time setup/teardown for an entire suite.
    ```typescript
    import { test, expect } from '@playwright/test';

    test.describe('User Authentication Flow', () => {
      test.beforeEach(async ({ page }) => {
        await page.goto('/login');
      });

      test('should allow a user to log in successfully', async ({ page }) => {
        await page.locator('[data-testid="username"]').fill('testuser');
        await page.locator('[data-testid="password"]').fill('password123');
        await page.locator('[data-testid="submit-button"]').click();
        await expect(page).toHaveURL('/dashboard');
      });

      test('should show error on invalid credentials', async ({ page }) => {
        // ... test logic for invalid login
      });
    });
    ```

3.  **API Mocking:**
    *   For deterministic and faster E2E tests, mock API requests using `page.route()`. This allows you to control API responses and avoid dependencies on live backend services.
    *   Mock responses should reflect realistic scenarios, including success cases, error cases, and edge cases.
    ```typescript
    test('should display products from API', async ({ page }) => {
      // Mock the API call for products
      await page.route('**/api/products', async route => {
        const json = [{ id: 1, name: 'Product A' }, { id: 2, name: 'Product B' }];
        await route.fulfill({ json });
      });

      await page.goto('/products');
      await expect(page.getByText('Product A')).toBeVisible();
      await expect(page.getByText('Product B')).toBeVisible();
    });
    ```

4.  **Assertions:**
    *   Use Playwright's built-in assertions (`expect()`) for clear and readable checks.
    *   Assert on user-visible outcomes rather than implementation details (e.g., check if text is visible, if an element has a certain role, if navigation occurs, rather than checking internal component state).
    *   Use auto-retrying assertions (`expect(locator).toBeVisible()`) which wait for conditions to be met, reducing flakiness.

5.  **Test Data Management:**
    *   Avoid hardcoding sensitive or highly dynamic test data directly in tests.
    *   Consider strategies for managing test data, such as:
        *   Using fixtures or helper functions to generate test data.
        *   Fetching test data from a dedicated test API endpoint if necessary.
        *   Cleaning up created test data in `afterEach` or `afterAll` hooks to ensure test independence.

6.  **CI/CD Integration:**
    *   Ensure E2E tests are integrated into the CI/CD pipeline to run automatically on every commit or pull request.
    *   Configure reporting (e.g., Playwright's HTML reporter) to easily diagnose failures in CI.
    *   Consider parallel execution of tests in CI to speed up the feedback loop.

7.  **Page Object Model (POM) - For Larger Projects:**
    *   For larger applications, consider implementing the Page Object Model design pattern.
    *   Create classes representing pages or major components of your application. These classes encapsulate the selectors and methods for interacting with that part of the UI.
    *   This improves test maintainability and reduces code duplication.
    ```typescript
    // Example: LoginPage.ts (Page Object)
    // export class LoginPage {
    //   constructor(private page: Page) {}
    //
    //   async login(username, password) {
    //     await this.page.locator('[data-testid="username"]').fill(username);
    //     await this.page.locator('[data-testid="password"]').fill(password);
    //     await this.page.locator('[data-testid="submit-button"]').click();
    //   }
    // }
    ```

## General Testing Principles (Applicable to Unit & Integration Tests too):

*   **Test Independence:** Tests should be independent and runnable in any order. One test should not depend on the state or outcome of another.
*   **Readability:** Write tests that are easy to read and understand. The test itself should clearly document what it's testing and why.
*   **Speed:** Aim for fast test execution to provide quick feedback to developers.
*   **Determinism:** Tests should produce the same result every time they are run with the same code and environment (avoid flakiness).
*   **Coverage:** Strive for good test coverage, but prioritize testing critical paths and complex logic. 100% coverage is not always practical or necessary, but key functionalities must be covered.

This section provides guidelines for the Testing Agent to ensure the application is thoroughly tested and reliable.
