## 1. The Internet: login form for a live demo

**https://the-internet.herokuapp.com/login.** Fits slides 56–62: it is also a login form, and the login and password are written right on the page (`tomsmith` / `SuperSecretPassword!`).

| ID | Type | Data | Expected result |
|---|---|---|---|
| TC-01 | Positive | tomsmith / SuperSecretPassword! | /secure opens, message "You logged into a secure area!" |
| TC-02 | Negative | tomsmith / wrong123 | "Your password is invalid!", the user stays on /login |
| TC-03 | Negative | anna / SuperSecretPassword! | "Your username is invalid!" |
| TC-04 | Negative | empty fields | "Your username is invalid!" |
| TC-05 | Boundary | " tomsmith " with spaces | Are the spaces trimmed? A good question for the analyst |
| TC-06 | Positive | log in, then Logout | "You logged out of the secure area!", /secure is no longer accessible |

This site makes it easy to show the difference from the form on the slide: here the message reveals which field is wrong ("username is invalid"). Compare it with TC-06 on slide 61 and ask the students whether this is a bug. A good opportunity to talk about security and the oracle.

## 2. SauceDemo: a shop with real bugs for a bug report

**https://www.saucedemo.com.** All passwords are `secret_sauce`, and the users are listed on the page. The main one is the `problem_user`, who has bugs built in on purpose. Ideal material for slide 65.

| ID | Type | Data | Expected result |
|---|---|---|---|
| TC-01 | Positive | standard_user | The product list (Products) opens |
| TC-02 | Negative | locked_out_user | "Epic sadface: Sorry, this user has been locked out." |
| TC-03 | Negative | empty username | "Epic sadface: Username is required" |
| TC-04 | Negative | standard_user / wrong password | "Username and password do not match any user in this service" |
| TC-05 | Positive | add 2 products to the cart | The cart badge shows 2 |
| TC-06 | Negative | checkout with an empty First Name | "Error: First Name is required" |
| TC-07 | Positive | complete checkout | "Thank you for your order!" |

Bugs to demonstrate with `problem_user`:
- all products have the same image;
- sorting does not work;
- during checkout, typing in Last Name corrupts First Name.

You can open two windows, one with `standard_user` and one with `problem_user`, and ask the students to find the differences. This also serves as the "existing system" oracle from slide 25.

Example bug report to analyze:

> **BUG-01. Checkout: text from Last Name ends up in First Name (problem_user)**
> Environment: saucedemo.com · Chrome · Windows 11
> Steps: 1) log in as problem_user; 2) add a product and click Checkout; 3) enter "Anna" in First Name and "Test" in Last Name.
> Expected: the fields contain "Anna" and "Test". Actual: Last Name is empty, First Name has changed.
> Severity: High · Priority: P1 · Attachment: screen recording.

## 3. DemoQA Practice Form: a sample for the homework

**https://demoqa.com/automation-practice-form.** This exact form is given in Homework 1, so in the lecture show 3–4 cases as a sample, and the students write the rest themselves.

| ID | Type | Data | Expected result |
|---|---|---|---|
| TC-01 | Positive | all required fields: first name, last name, gender, 10-digit phone | A "Thanks for submitting the form" window with the entered data |
| TC-02 | Negative | empty First Name | The form is not submitted, the field is highlighted in red |
| TC-03 | Boundary | 9-digit phone | The form is not submitted |
| TC-04 | Boundary | 11-digit phone | Only 10 digits are accepted |
| TC-05 | Negative | email "anna@" | The field is highlighted in red, the form is not submitted |

The phone field illustrates the boundary values from slide 62 well: we check 9, 10 and 11 digits.
