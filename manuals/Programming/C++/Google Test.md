# Assertions
To determine whether a test should pass or fail, we use assertion macros. There are two main types of assertions: 

- `ASSERT_*` - generates a fatal failure when it fails, aborting the current function
- `EXPECT_*` - generates a nonfatal failure, allowing the function to continue running


## Basic Assertions

- `_EQ(computed, expected)` - tests that `expected == actual`. `==` must be defined for the type of the arguments.