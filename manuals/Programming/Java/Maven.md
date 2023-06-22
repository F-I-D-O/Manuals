# Dependencies
All Maven dependencies should work out of the box. If some dependencies cannot be resolved:
- check that the dependencies are on the maven central.
- if not, check that they are in some special repo and check that the repo is present in the pom of the project that requires the dependency

# Compilation
[reference](https://maven.apache.org/plugins/maven-compiler-plugin/compile-mojo.html)

Compilation is handeled by the Maven compiler plugin. Usually, typing `mvn compile` is enough to compile the project.

If you need any customization, add it to the compiler plugin configuration
```XML
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-compiler-plugin</artifactId>
	<version>3.10.1</version>
	<configuration>
		....
	</configuration>
</plugin>
```

## Passing arguments to `javac`
A single argument can be passed using the `<compilerArgument>` property. For more compiler arguments, use `<compilerArgs>`:
```XML
<compilerArgs>
	<arg>-Xmaxerrs=1000</arg>
	<arg>-Xlint</arg>
</compilerArgs>

```


# Tests
Tests are usually executed with the Maven Surefire plugin using the `test` goal.

## Run a single tests file
To run a single test file, use:
```
mvn test -Dtest="<TEST CLASS NAME>"
```
The name should be just a class name without the package and without file extension:
```
mvn test -Dtest="OSMFileTest"
```

We can also use a fully qualified name, if there are more test classes with the same name:

```
mvn test -Dtest="cz.cvut.fel.aic.roadgraphtool.procedures.input.OSMFileTest"
```

## Run tests using a pattern
More test can be run with a pattern, for example:
```
mvn test -Dtest="cz.cvut.fel.aic.roadgraphtool.procedures.input.**"
```
runs all tests within the `input` package.


# Execute Programs from Maven
For executing programs, Maven has the exec target. Mostly, you need to exacute java programs from maven. Basic example:
```
mvn exec:java  -Dexec.mainClass=test.Main
```
Other usefull arguments:
 - `-Dexec.args="arg1 arg2 arg3"`
 
If you want to pass the arguments like `Xmx` to jvm, you cannot use the `java` subgoal of the exec command. That is because with the `java` subgoal, Maven uses the same jvm it is running in to execute the program. To conigure jvm, we need to start a new instance. That is possible with the `exec` subgoal:

```
mvn exec:exec -Dexec.executable="java" -Dexec.args="Xmx30g -classpath %classpath test.Main"
```
**Note that here, the `-Dexec.args` parameter is used both for vm and runtime arguments.**

We can also use `-Dexec.mainClass` with `exec:exec`, but we need to refer it in the `-classpath` argument. The following three maven commands run the same Java program:
```
mvn exec:java  -Dexec.mainClass=test.Main

mvn exec:exec -Dexec.executable="java" -Dexec.args="-classpath %classpath test.Main"

mvn exec:exec -Dexec.executable="java" -Dexec.mainClass=test.Main -Dexec.args="-classpath %classpath ${exec.mainClass}"
```




# HTTPS certificates
Sometimes, it can happen that maven cannot connect to a repository with this error:
```
PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

This error signals that the server SSL certificate of the maven repo (when using HTTPS) is not present in the local SSL certificate keystore. This can have two reasons, to disintiguish between them, try to access the repo from your browser over https:
- If you can access the repo from your browser, it means that the server has a valid SSL certificate, but it is not in zour local keystore (just in the browser keystore). You can solve this problem by adding the certificate to your java SSL keystore (see below).
- if you cannot access the server from your browser, it is likely that the server does not have a valid SSL certificate, and you have to solve it on the serer side.

## Adding a new SSL certificate to your keystore
1. Open the repo URL in your browser 
2. Export the certificate:
	- Chrome: click on the padlock icon left to address in address bar, select `Certificate -> Details -> Copy to File` and save in format "Der-encoded binary, single certificate".
	- Firefox: click on HTTPS certificate chain (the lock icon right next to URL address). Click `more info -> security -> show certificate -> details -> export..`. Pickup the name and choose file type `*.cer`
3. Determine the keystore location:
	3.1 Using `maven --version`, find out the location of the java used by Maven
	3.2 The keystore is saved in file:`<JAVA LOCATION>/lib/security/cacerts`
4. Open console as administrator and add the certificate to the keystore using:
```
keytool -import -keystore "<PATH TO cacerts>" -file "PATH TO TH EXPORTED *.cer FILE"
```

You can check that the operation was sucessful by listing all certificates:
```
keytool -keystore "<PATH TO cacerts>" -list
```

# Debugging maven
First, try to look at the versions of related dependencies and plugins. Old versions of these can cause many problems.

## No tests found using the `Dtest` argument of the `test` goal
1. Check the class name/path/pattern
2. If the name works, but pattern does not, it can be caused by an old version of the surefire plugin that use a different patten syntax.

## uncompilable  source code
Try to clean and compile again