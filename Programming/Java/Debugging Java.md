# General rules
1. Warnings can help you to spot the problems. Check that they are enabled (`Xlint`).
1. Sometimes, warnings may help to understand the problem. However, they are not emmited due to compilation error. Try to comment out the errorneous code and compile the code to see all warnings.


# Missing Resources
First, check if the resources are where you expected in the `jar` or in the `target` folder. The structure is described [here on SO](https://stackoverflow.com/questions/7613359/why-cant-i-access-src-test-resources-in-junit-test-run-with-maven).

If the resources are not there, try to rebuild the project.
