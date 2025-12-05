## 1. Document Overview

- Document type: Assignment/Practice Questions for an online certification course.
- Main purpose or goal of the document: To assess understanding of fundamental mathematical concepts pertinent to machine learning, specifically covered in Week 3 of the NPTEL "Mathematics for Machine Learning 2025" course.
- Approximate scope:
  - Number of pages: 5 pages.
  - High-level topics covered: Directional derivatives, gradients, convex functions, gradient descent algorithm, subgradient descent, and first-order Taylor approximation, often in the context of loss functions.
- One paragraph high-level summary: This document presents a set of 10 multiple-choice/multiple-select questions designed for Week 3 of the "Mathematics for Machine Learning 2025" NPTEL course. Each question tests knowledge of key calculus and optimization concepts foundational to machine learning, such as calculating directional derivatives and gradients, understanding the properties of convex functions, applying gradient descent principles (including stopping criteria and update rules), and recognizing the first-order Taylor approximation. Solutions are provided for each question, referencing specific lectures within Week 3.

## 2. Detailed Section-by-Section Summary

The document is structured as a series of multiple-choice/multiple-select questions with provided solutions. Each "section" below corresponds to one question.

- **Question 1: Directional Derivative Calculation**
  - **Page range:** Page 1
  - **Summary:** This question asks for the directional derivative of a linear function, `f(x, y) = 5x + 7y`, in a specific direction `(2, 0)`. The solution demonstrates the calculation using the limit definition of the directional derivative. It shows how to substitute `w = (w1, w2)` and `d = (d1, d2)` into the formula `lim(h→0) [f(w1+hd1, w2+hd2) - f(w1, w2)] / h`, simplifying the expression to `(5d1 + 7d2)`. For the given direction `(2, 0)`, the derivative is `5 * 2 + 7 * 0 = 10`.
  - **Reference:** Lecture 3.1 of Week 3.

- **Question 2: Gradient of a Scalar Function**
  - **Page range:** Page 1-2
  - **Summary:** The question asks for the gradient of the function `f(x1, x2) = x1^3 - x2`. The solution calculates the gradient vector by finding the partial derivatives with respect to `x1` and `x2`. The partial derivative `∂f/∂x1` is `3x1^2`, and `∂f/∂x2` is `-1`. Thus, the gradient `∇f(x1, x2)` is `(3x1^2, -1)`.
  - **Reference:** Not explicitly stated but standard calculus.

- **Question 3: Direction of Most Rapid Change**
  - **Page range:** Page 2
  - **Summary:** This question concerns the relationship between the directional derivative `f'(w, d)`, the gradient `∇f(w)`, and the direction vector `d`. It states the formula `f'(w, d) = ||∇f(w)|| ||d|| cos θ`, where `θ` is the angle between `∇f(w)` and `d`. The question asks which statement about the direction of most rapid increase is true. The correct answer highlights that a function `f` increases most rapidly at a point `w` in the direction of its gradient (`∇f(w)`) when `θ = 0`, meaning `d` is aligned with `∇f(w)`.
  - **Reference:** Lecture 3.2 of Week 3.

- **Question 4: Properties of Convex Functions**
  - **Page range:** Page 2
  - **Summary:** This question explores properties of convex functions, specifically how derivatives/subgradients behave with sums and scalar multiples. Given that `f1, f2, ..., fm` are convex functions and `f = f1 + f2 + ... + fm`, it asks which statement is true about `∂f(x)` (or `df(x)` representing the subgradient/derivative). The solution states that the subgradient of a sum of convex functions is the sum of their individual subgradients: `df(x) = df1(x) + df2(x) + ... + dfm(x)`. It also clarifies that for a scalar `c > 0`, `d(cf(x)) = c df(x)`. Based on these rules, `d(2f(x)) = 2df(x)` and `d(3f(x)) = 3df(x)` are correct.
  - **Reference:** Lecture 3.5 of Week 3.

- **Question 5: Direction of Most Rapid Decrease**
  - **Page range:** Page 3
  - **Summary:** This question asks for the direction `(α, β)` in which the function `f(x, y) = x^2 + y` decreases most rapidly at the point `(1, 0)`. The solution first calculates the gradient `∇f(x, y) = (∂f/∂x, ∂f/∂y) = (2x, 1)`. At the point `(1, 0)`, the gradient is `∇f(1, 0) = (2, 1)`. The direction of most rapid decrease is the negative of the gradient, `-∇f(1, 0) = -(2, 1)`. To express this as a unit vector (or a direction vector), it is normalized: `v = -(2 / sqrt(2^2 + 1^2), 1 / sqrt(2^2 + 1^2)) = (-2/√5, -1/√5)`.
  - **Reference:** Lecture 2 of Week 3.

- **Question 6: Gradient Descent Stopping Criteria**
  - **Page range:** Page 3
  - **Summary:** This question asks to identify the *false* statement regarding the stopping criteria for the gradient descent algorithm. The solution lists the common stopping criteria:
    1.  The change in weights between iterations is small: `||w^(k+1) - w^(k)|| ≤ ε`.
    2.  The norm of the gradient at the current weights is small: `||∇f(w^(k))|| ≤ ε`.
    3.  The change in the objective function value between iterations is small: `||f(w^(k+1)) - f(w^(k))|| ≤ ε`.
    The false statement is `||w^(k) - w^(k-1)|| ≥ ε`, as this would imply *continuing* to iterate if the change is large, not stopping if it's small.
  - **Reference:** Lecture 3.3, Week 3.

- **Question 7: Sub-gradient Descent and Loss Functions**
  - **Page range:** Page 4
  - **Summary:** This question addresses the differentiability of common machine learning loss functions and the applicability of sub-gradient descent. The correct statement is that the sub-gradient descent algorithm *can* be used to find the optimal solution in Lasso regression. The solution clarifies that the loss functions for Lasso regression and Support Vector Machines (SVMs) are *not* differentiable everywhere (due to terms like `|w|` in Lasso or hinge loss in SVM). Therefore, standard gradient descent cannot be directly applied, but sub-gradient descent, which handles non-differentiable points by using subgradients, can be used.
  - **Reference:** Lecture 3.5, Week 3.

- **Question 8: Gradient of a Vector-Valued Function (Jacobian Matrix)**
  - **Page range:** Page 4
  - **Summary:** This question asks for the "gradient" of a vector-valued function `f(x, y) = (f1, f2) = (2x^2y + xy^2, x^2y + 3xy^2)`. For a vector-valued function, the "gradient" is represented by the Jacobian matrix. The solution calculates the partial derivatives of each component function (`f1` and `f2`) with respect to `x` and `y`.
    - `∂f1/∂x = 4xy + y^2`
    - `∂f1/∂y = 2x^2 + 2xy`
    - `∂f2/∂x = 2xy + 3y^2`
    - `∂f2/∂y = x^2 + 6xy`
    The Jacobian matrix `∇f(x, y)` is then `[[∂f1/∂x, ∂f1/∂y], [∂f2/∂x, ∂f2/∂y]]`.
  - **Reference:** Lecture 2 of Week 3.

- **Question 9: Gradient Descent Update Rule**
  - **Page range:** Page 4-5
  - **Summary:** This question asks for the correct update rule for weights `w` in the gradient descent method, where `w^(k)` are the current weights, `α` is the learning rate, and `f` is the objective function to minimize. The solution provides the standard gradient descent update rule: `w^(k+1) = w^(k) - α∇f(w^(k))`. This rule indicates that the new weights are obtained by subtracting a step in the direction of the negative gradient (the direction of steepest decrease), scaled by the learning rate.
  - **Reference:** Lecture 3 of Week 3.

- **Question 10: First-Order Taylor Approximation**
  - **Page range:** Page 5
  - **Summary:** This question asks for the first-order Taylor approximation of a function `f` around a point `w`. The correct formula for the first-order Taylor approximation of `f(x)` around `w` is `f(x) ≈ f(w) + ∇f(w)(x - w)`. This linear approximation uses the function value and its gradient at the point `w` to estimate the function value at a nearby point `x`.
  - **Reference:** Lecture 4 of Week 3, also Lecture 2 of Week 3.

## 3. Key Ideas, Claims, and Takeaways

-   **Key Idea 1 – Directional Derivatives**
    -   **What the idea/claim is:** The directional derivative measures the rate at which a function changes in a specific direction. It can be calculated using the limit definition or, for differentiable functions, as the dot product of the gradient and a unit direction vector.
    -   **Why it matters in the context of the document:** It's a fundamental concept in multivariable calculus essential for understanding how functions behave in different directions, which is crucial for optimization algorithms.
    -   **Where it appears:** Question 1 (Page 1).
    -   **Evidence:** The solution in Question 1 provides a step-by-step calculation of the directional derivative for a given linear function using the limit definition.

-   **Key Idea 2 – Gradient and Steepest Change**
    -   **What the idea/claim is:** The gradient vector `∇f(w)` points in the direction of the greatest rate of increase of a function `f` at a point `w`. Conversely, the negative gradient `-∇f(w)` points in the direction of the greatest rate of decrease (steepest descent). The magnitude of the gradient represents the maximum rate of change.
    -   **Why it matters in the context of the document:** This concept is central to optimization algorithms like gradient descent, where the goal is to find the minimum of a function by moving in the direction of steepest descent.
    -   **Where it appears:** Question 2 (Page 1-2), Question 3 (Page 2), Question 5 (Page 3).
    -   **Evidence:** Question 2 demonstrates how to compute the gradient. Question 3 states the relationship between directional derivative and gradient (`f'(w,d) = ||∇f(w)|| ||d|| cos θ`). Question 5 applies the concept to find the direction of most rapid decrease.

-   **Key Idea 3 – Gradient Descent Algorithm**
    -   **What the idea/claim is:** Gradient descent is an iterative optimization algorithm used to find the local minimum of a differentiable function. It proceeds by taking steps proportional to the negative of the gradient of the function at the current point. The update rule is `w^(k+1) = w^(k) - α∇f(w^(k))`, where `α` is the learning rate. The algorithm stops when certain criteria (e.g., small change in weights, small gradient norm, small change in objective function) are met.
    -   **Why it matters in the context of the document:** Gradient descent is a core optimization algorithm in machine learning, and understanding its mechanics, including the update rule and stopping conditions, is fundamental.
    -   **Where it appears:** Question 6 (Page 3), Question 9 (Page 4-5).
    -   **Evidence:** Question 9 explicitly states the correct update rule. Question 6 lists the common stopping criteria for the algorithm.

-   **Key Idea 4 – Subgradient Descent for Non-Differentiable Functions**
    -   **What the idea/claim is:** Some important loss functions in machine learning, such as those used in Lasso regression or Support Vector Machines, are not differentiable at all points. For such functions, the concept of a subgradient is used, and optimization can be performed using subgradient descent, which generalizes gradient descent to non-differentiable functions.
    -   **Why it matters in the context of the document:** This highlights a practical consideration in applying optimization methods in machine learning, extending beyond simple differentiable functions.
    -   **Where it appears:** Question 7 (Page 4).
    -   **Evidence:** The solution in Question 7 states that Lasso regression and SVM loss functions are not differentiable, but sub-gradient descent can be used for them.

-   **Key Idea 5 – First-Order Taylor Approximation**
    -   **What the idea/claim is:** The first-order Taylor approximation provides a linear approximation of a function around a given point. It uses the function's value and its first derivative (gradient for multivariable functions) at that point to estimate the function's value at a nearby point: `f(x) ≈ f(w) + ∇f(w)(x - w)`.
    -   **Why it matters in the context of the document:** Taylor approximations are crucial for understanding and deriving many optimization algorithms and for analyzing function behavior locally.
    -   **Where it appears:** Question 10 (Page 5).
    -   **Evidence:** The correct formula for the first-order Taylor approximation is provided as the solution to Question 10.

## 4. Important Tables (with page numbers)

No tables are present in this document.

## 5. Important Images / Figures (with page numbers)

No significant figures are present in this document, only institutional logos and header text.

## 6. Concepts, Definitions, and Terminology

-   **Term:** Directional Derivative
    -   **Page(s):** 1
    -   **Explanation:** The rate at which a function's value changes at a given point in a specified direction. It can be computed by taking the dot product of the function's gradient with a unit vector in the specified direction, or by using the limit definition.
    -   **Role in the document:** Central to Question 1, demonstrating a fundamental calculus concept for understanding function behavior.

-   **Term:** Gradient
    -   **Page(s):** 1, 2, 3, 4, 5
    -   **Explanation:** For a scalar-valued function of several variables, the gradient is a vector whose components are the partial derivatives of the function with respect to each variable. It points in the direction of the greatest rate of increase of the function. For vector-valued functions, it extends to the Jacobian matrix.
    -   **Role in the document:** A core concept appearing in most questions. It's used for calculating steepest ascent/descent, in the gradient descent algorithm, and in Taylor approximations.

-   **Term:** Convex Function
    -   **Page(s):** 2
    -   **Explanation:** A function for which the line segment connecting any two points on its graph lies above or on the graph itself. For differentiable functions, this means the second derivative (or Hessian matrix) is positive semi-definite.
    -   **Role in the document:** Discussed in Question 4 regarding how derivatives/subgradients combine for sums and scalar multiples of convex functions.

-   **Term:** Subgradient
    -   **Page(s):** 2, 4
    -   **Explanation:** A generalization of the gradient for non-differentiable convex functions. At a point where a function is differentiable, the subgradient is unique and equal to the gradient. At non-differentiable points, a set of subgradients exists.
    -   **Role in the document:** Essential for understanding how to optimize non-differentiable loss functions in machine learning, as covered in Question 7.

-   **Term:** Gradient Descent
    -   **Page(s):** 3, 4, 5
    -   **Explanation:** An iterative optimization algorithm used to minimize an objective function by moving in the direction opposite to the function's gradient. It updates parameters `w` by `w^(k+1) = w^(k) - α∇f(w^(k))`.
    -   **Role in the document:** The central optimization algorithm discussed, with questions on its stopping criteria (Q6) and update rule (Q9).

-   **Term:** Learning Rate (α)
    -   **Page(s):** 4
    -   **Explanation:** A hyperparameter in optimization algorithms like gradient descent that determines the step size at each iteration while moving towards a minimum of a loss function.
    -   **Role in the document:** Appears in the gradient descent update rule in Question 9.

-   **Term:** Stopping Criteria
    -   **Page(s):** 3
    -   **Explanation:** Conditions that determine when an iterative algorithm, such as gradient descent, should terminate. Common criteria include a small change in parameters, a small gradient norm, or a small change in the objective function value.
    -   **Role in the document:** Explicitly questioned in Question 6, highlighting practical aspects of implementing optimization algorithms.

-   **Term:** Lasso Regression
    -   **Page(s):** 4
    -   **Explanation:** A linear regression method that uses L1 regularization, which adds a penalty equal to the absolute value of the magnitude of coefficients. This can lead to sparse models where some coefficients become zero, effectively performing feature selection.
    -   **Role in the document:** Used as an example of a machine learning model whose loss function is non-differentiable, requiring subgradient descent (Q7).

-   **Term:** Support Vector Machine (SVM)
    -   **Page(s):** 4
    -   **Explanation:** A supervised learning model that uses classification and regression analysis to find a hyperplane that best separates data points into classes in a high-dimensional space. The optimization involves maximizing the margin between classes.
    -   **Role in the document:** Another example of a machine learning model whose loss function (hinge loss) is non-differentiable, making it suitable for subgradient descent (Q7).

-   **Term:** First-Order Taylor Approximation
    -   **Page(s):** 5
    -   **Explanation:** A linear approximation of a function `f(x)` around a point `w`, given by `f(x) ≈ f(w) + ∇f(w)(x - w)`. It uses the function's value and its gradient at `w` to estimate values nearby.
    -   **Role in the document:** Tested in Question 10 as a fundamental mathematical tool for analyzing and approximating functions.

## 7. Constraints, Limitations, and Open Questions

The document itself is a set of questions and solutions for an assignment. As such, it does not state any limitations, assumptions, open problems, or caveats of the concepts it covers, beyond the implicit assumption that the concepts are being taught within the scope of the "Mathematics for Machine Learning" course. The solutions refer to specific lectures, implying that detailed explanations, assumptions, and broader context are provided within those lectures.

## 8. Notes for the Storytelling / Presentation Agent

-   **Key Ideas to Emphasize:**
    -   **Technical Audience:** Emphasize all Key Ideas (1-5). The practical implications of non-differentiable loss functions (Key Idea 4) and the details of gradient descent (Key Idea 3) are particularly important. The mathematical foundations (directional derivatives, gradients, Taylor approximations) are also critical.
    -   **Non-Technical Audience:** Focus on Key Idea 3 (Gradient Descent) as the core optimization method used in ML, explaining its purpose (finding minimums) and the idea of "stepping down the hill." Briefly touch upon the concept of a "gradient" as the direction of steepest change. Key Idea 4 (Subgradient Descent) could be simplified to "sometimes functions aren't smooth, so we need a slightly different version of gradient descent."

-   **Best Candidates for Embedding in a Story/Slide Deck:**
    -   There are no tables or figures in the document itself to embed. However, the *concepts* lend themselves well to visual representation:
        -   **Gradient Descent Visualization:** A 3D plot of a function with contours, showing the path of gradient descent iterations (linked to Q6 & Q9).
        -   **Gradient Vector Field:** A plot showing gradient vectors at various points on a function's surface to illustrate the direction of steepest ascent/descent (linked to Q3 & Q5).
        -   **Non-Differentiable Loss Function:** A simple plot of an absolute value function or hinge loss to illustrate points where a gradient doesn't exist but a subgradient does (linked to Q7).
        -   **Taylor Approximation Plot:** A plot showing a function and its linear (first-order Taylor) approximation at a point (linked to Q10).

-   **Natural Narrative Arcs:**
    -   **"From Calculus to Optimization in ML":** Start with basic calculus tools (gradients, directional derivatives, Taylor approximation) that describe function behavior. Transition to how these tools are used in optimization algorithms like Gradient Descent to train ML models. Discuss practical considerations like stopping criteria and handling non-differentiable loss functions.
    -   **"The Mechanics of Learning: How ML Models Find the Best Fit":** Introduce the idea of an objective/loss function. Explain how gradient descent is the "engine" that minimizes this function to find the optimal model parameters. Detail the steps of gradient descent and what tells it to stop. Mention how it adapts for complex, "non-smooth" problems.

-   **Sections to Downplay or Skip:**
    -   Since the document consists of core concepts, no sections should be entirely downplayed. However, the detailed mathematical derivations (e.g., the full limit calculation in Q1) could be simplified for a non-technical audience, focusing on the result and its interpretation rather than the algebraic steps.