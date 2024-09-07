Maven is a dependency management and build tool for Java. 

The project configuration for Maven is stored in a single file called `pom.xml`. Both the project dependencies and the build configuration are stored in this file.

The maven is executed using the as `mvn <goal>`. Typical goals are

- `compile`: compile the project
- `test`: run tests
- `package`: package the project into a jar or war file
- `install`: install the project into the local maven repository
- `deploy`: deploy the project to a remote repository


# Maven Packages: Artifacts
All Maven dependencies and plugins installed in local system repositories can be either:

- downloaded from a remote repository
- installed from a local file or project

Note that if we want the artifact to be downloaded from a remote repository, we do not have to take any action. It will be downloaded automatically when needed.

By default, Maven searches for artifacts in the [Maven Central repository](https://central.sonatype.com/). If we want to use a different repository, we have to add it manually.


## List locally installed artifacts
There is no built-in command to list all locally installed artifacts. However, we can use the [info plugin](https://github.com/F-I-D-O/info-maven-plugin):
```bash
mvn ninja.fido:info-maven-plugin:list
```


## Install artifacts from a remote repository manually
If we want to install an artifact from a remote repository manually, we can use the `dependency:get` goal. The syntax is as follows:
```bash
mvn dependency:get -Dartifact=<GROUP ID>:<ARTIFACT ID>:<VERSION>
```


## Debugging missing Artifacts
All Maven dependencies should work out of the box. If some dependencies cannot be resolved:

- check that the dependencies are on the maven central.
- if not, check that they are in some special repo and check that the repo is present in the pom of the project that requires the dependency



# Variables
Variables in the `pom.xml` file can be used using the `${variable}` syntax. 

To use some environment variables, we can use the `${env.variable}`.

Note that contrary to all expectations, **maven goals do not fail if a variable is not defined**. Instead, the variable is replaced with an empty string. This can lead to unexpected behavior, so it is usually preferable to fail. For that, we can use the [enforcer plugin](https://maven.apache.org/enforcer/) with the `requireProperty` rule:
```XML
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-enforcer-plugin</artifactId>
	<version>3.4.1</version>
	<executions>
	<execution>
		<id>enforce-property</id>
		<goals>
			<goal>enforce</goal>
		</goals>
		<configuration>
			<rules>
				<requireProperty>
					<property>basedir</property>
					<message>You must set a basedir property!</message>
				</requireProperty>
			</rules>
			<fail>true</fail>
		</configuration>
	</execution>
	</executions>
</plugin>
```

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



# Dependencies
Maven dependencies are defined in the `pom.xml` file, in the `<dependencies>` section. Each dependency has the following structure:
```XML
<dependency>
	<groupId>org.apache.maven</groupId>
	<artifactId>maven-core</artifactId>
	<version>3.0</version>
	<scope>compile</scope>
</dependency> 
```
The `scope` property is optional and the default value is `compile`. 

The dependencies are automatically downloaded if we run a maven goal that requires them (e.g., `compile`, `test`, `install`). If we want to download them manually, we can use the `dependency:resolve` goal.

To list all dependencies of a project, we can use the `dependency:list` goal.


## Using dependencies distributed as a jar
Sometimes, we possess a jar file that is not present in any maven repository. We can still install it to the local repository as a new artifact using the `install:install-file` goal:
```bash
mvn install:install-file -Dfile=<PATH TO JAR> -DgroupId=<GROUP ID> -DartifactId=<ARTEIFACT ID> -Dversion=<VERSION> -Dpackaging=jar
```
Here the `<PATH TO JAR>` is a path to the jar library. The `<GROUP ID>`, `<ARTEIFACT ID>`, and `<VERSION>` can have arbitrary values, they just have to correspond with the values specified in the pom dependency.

Be careful with PowerShell: in PowerShell, program parameters starting with minus and containing dot need to be quoted, for example: `'-DgroupId=com.example.app'` instead of `-DgroupId=com.example.app`


## Using dependencies distributed as a zip
Sometimes, the dependency is distributed as a zip file containing sources.
Typically, the manual for such a library tells us to modify the classpath to include the sources. However, Maven handles the classpath automatically, so it is not wise to modify it manually. The best way to use it is to unpack the zip and add the sources to the project during compilation. For that, we can use the `build-helper-maven-plugin` plugin:
```XML
<plugin>
	<groupId>org.codehaus.mojo</groupId>
	<artifactId>build-helper-maven-plugin</artifactId>
	<version>3.2.0</version>
	<executions>
		<execution>
			<id>add-lib-sources</id>
			<phase>generate-sources</phase>
			<goals>
				<goal>add-source</goal>
			</goals>
			<configuration>
				<sources>
					<source>path/to/lib/folder</source>
				</sources>
			</configuration>
		</execution>
	</executions>
</plugin>
```


# Tests
Tests are usually executed with the Maven Surefire plugin using the `test` goal.


## Test configuration
Tests are run using the [Maven Surefire plugin](https://maven.apache.org/surefire/maven-surefire-plugin/). Usually, the default configuration is enough. However, if we want to customize the test execution, we can add the plugin to our pom and configure it:
```XML
<build>
	<plugins>
		<plugin>
			<groupId>org.apache.maven.plugins</groupId>
			<artifactId>maven-surefire-plugin</artifactId>
			<version>3.0.0-M5</version>
			<configuration>
				... configuration ...
			</configuration>
		</plugin>
	</plugins>
	... other plugins ...
</build>
```

For example, to exclude some tests, the following configuration can be used:
```XML
<configuration>
	<excludes>
		<exclude>**/IncompleteTest.java</exclude>
	</excludes>
</configuration>
```

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
For executing programs, Maven has the `exec` plugin. This plugin has two goals: 

- `exec:java`: for Java programs
- `exec:exec`: for any program

However, the `exec:java` goal is not very flexible. It uses the same JVM as the calling Maven process, so the JVM cannot be configured in any way. Notably, with the `exec:java` goal, it is not possible to:

- pass JVM arguments like `-Xmx`
- set the library path using `-Djava.library.path`

Note that when working with PowerShell, we typically encounter the problem with arguments that start with `-` and contain a dot. For guide how to solve this, refer to the [PowerShell manual](../../Windows/Powershell%20Manual.md).

## `exec:java`
Basic example:
```
mvn exec:java  -Dexec.mainClass=test.Main
```
Other usefull arguments:
 - `-Dexec.args="arg1 arg2 arg3"`
 
## `exec:exec`
Basic example:
```
mvn exec:exec -Dexec.executable="java" -Dexec.args="Xmx30g -classpath %classpath test.Main"
```
The `-classpath %classpath` argument is obligatory and it is used to pass the project classpath to the program. 

**Note that here, the `-Dexec.args` parameter is used both for vm and program arguments.** The order is:

1. JVM arguments, classpath
2. main class
3. program arguments
Example:
```
mvn exec:exec -Dexec.executable="java" -Dexec.args="-Xmx30g -classpath %classpath test.Main arg1 arg2"
```

We can also use `-Dexec.mainClass` with `exec:exec`, but we need to refer it in the `-classpath` argument. The following three maven commands run the same Java program:
```
mvn exec:java  -Dexec.mainClass=test.Main

mvn exec:exec -Dexec.executable="java" -Dexec.args="-classpath %classpath test.Main"

mvn exec:exec -Dexec.executable="java" -Dexec.mainClass=test.Main -Dexec.args="-classpath %classpath ${exec.mainClass}"
```

## Configure the exec plugin in the pom
We can add a configuration of the exec plugin to the `pom.xml`, so we do not have to type the arguments or the main class every time we run the program. However, this way, we have to supply all program arguments in the `pom.xml` file. **It is not possible to pass some parameters from the command line and some from the `pom.xml` file configuration.** Note that when using the `exec:ecec` goal, this includes the JVM arguments as well.





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



# Project Publishing
This section s focused on Maven projects but most of the steps should apply to all Java projects.

Steps:

1. Cleanup
1. Add License to all files
1. Test
1. Update Changelog
1. Update pom of the project and related projects
1. Install Locally
1. Deploy

## Cleanup
The following cleanup steps should be done:

- clean garbage/IDE files
	- check that they are in gitignore
	- remove already tracked files by `git rm -r --cached <path>`
- remove unused imports
	- In Netbeans: `Refactor` -> `Inspect and Transform` -> `browse` -> `imports` -> `organize imports`

## Add license information: 
There is a nice program called [licenseheaders](https://github.com/johann-petrak/licenseheaders) that can be used for that. Unfortunatelly, **the program is currently broken and a [fork](https://github.com/F-I-D-O/licenseheaders) must be used**. Syntax:
```bash
licenseheaders -t <license type> -o "<Owner>" -cy -n <Software name> -u "<link to github>" 
```	

A full path to a license template has to be given.


## Updating poms
In general, it is desirable to update the version of each related project from SNAPSHOT to the release version and then test the whole setup.

In complex setups, we need to:

1. Change the version of the parent project
2. Change the version of the project's dependencies
3. Change the version of the project itself
4. Update the versions of projects in parent pom
5. Update the versions of projects in the dependency section of each related project (if this is not done by the parent pom)

If we fullfill all these steps, we can deploy the project. Both SNAPSHOTs and releases can be deployed using the `deploy` goal. The repository is chosen based on the version of the artifact (SNAPSHOT or release).


## Deploying the project to Maven Central
Deploying to Maven Central has many advantages: it is free, reliable, and every maven user can get our artifact without any additional configuration. However, it is also a bit complicated due to security requirements and high quality standards. 

The process is usually as follows:

1. namespace (groupId) registration
2. deploying of artifacts to the namespace

Note that **for one group id registration, we can deploy multiple artifacts, as long as the registered group id is equal to, or a prefix of, the group id of the artifact**.

The whole process is described in detail in the [Central Repository Documentation](https://central-stage.sonatype.org/register/central-portal/). As of 2024-02-15, there is an ongoing migration from OSSRH to the new Central Portal. Because of that, we will describe the current (OSSRH) process only briefly, as it is likely to change in the future. Also, we will describe only the process for deploying artifacts, as the namespace registration in OSSRH is not possible anymore.

**To see your currently registered namespaces, go to the [your profile at sonatype Jira portal](https://issues.sonatype.org/secure/ViewProfile.jspa) and look insides the issues listed on right in the Activity Stream.**

### Deploying artifacts to OSSRH

Requirements:

- required metadata in the pom 
- javadoc and sources must be supplied
- all files must be signed with GPG
- various plugins and configuration need to be set up in the pom
- user authentication for the OSSRH must be set up in the `settings.xml` file

#### Required metadata
[Official documentation](https://central.sonatype.org/pages/requirements) (at the end)

The following metadata must be present in the pom:

- project tags:
	- `name`
	- `description`
	- `url`
- license information:
	```XML
	<licenses>
		<license>
			<name>MIT License</name>
			<url>https://opensource.org/licenses/MIT</url>
		</license>
	</licenses>

- developer information:
	```XML
	<developers>
		<developer>
			<name>Full Name</name>
			<email>user email</email>
			<url>user url</url>
		</developer>
	</developers>
	```

- scm information:
	```XML
	<scm>
		<connection>scm:git:git://github.com/simpligility/ossrh-demo.git</connection>
		<developerConnection>scm:git:ssh://github.com:simpligility/ossrh-demo.git</developerConnection>
		<url>http://github.com/simpligility/ossrh-demo/tree/master</url>
	</scm>
	```

#### Javadoc and sources setup
The following configuration is suitable for deploying with sources and javadoc:
```XML
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-source-plugin</artifactId>
	<version>2.2.1</version>
	<executions>
	<execution>
		<id>attach-sources</id>
		<goals>
		<goal>jar-no-fork</goal>
		</goals>
	</execution>
	</executions>
</plugin>
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-javadoc-plugin</artifactId>
	<version>2.9.1</version>
	<executions>
	<execution>
		<id>attach-javadocs</id>
		<goals>
		<goal>jar</goal>
		</goals>
	</execution>
	</executions>
</plugin>
```


#### Signing the artifacts with GPG
To sign the artifacts with GPG, we need to  add the gp plugin to the pom:
```XML
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-gpg-plugin</artifactId>
	<version>1.5</version>
	<executions>
	<execution>
		<id>sign-artifacts</id>
		<phase>verify</phase>
		<goals>
			<goal>sign</goal>
		</goals>
	</execution>
	</executions>
</plugin>
```
For this plugin to work, the GPG must be installed and available in the system path.

##### Storing the GPG passphrase
To make our life easier, we can store the GPG passphrase in the `settings.xml` file. The following configuration must be present in the `profiles` section:
```XML 
<profile>
	<id>ossrh</id>
	<activation>
		<activeByDefault>true</activeByDefault>
	</activation>
	<properties>
		<gpg.executable>gpg</gpg.executable> <!-- this should not be needed as gpg is default... -->
		<gpg.passphrase>F1D06949</gpg.passphrase>
	</properties>
</profile>
```


#### Required plugins and configuration
For the deployment to OSSRH, we need to use several plugins and add some configuration to the pom. First, we need to set up the distribution management:
```XML
<distributionManagement>
	<snapshotRepository>
		<id>ossrh</id>
		<url><SNAPSHOT URL></url>
	</snapshotRepository>
	<repository>
		<id>ossrh</id>
		<url><RELEASE URL></url>
	</repository>
</distributionManagement> 
```

The <SNAPSHOT URL> and <RELEASE URL> are links to the repo we have received after the namespace registration approval. Note that we need to use the original URLs, even if they do not match the links in the documentation. The current (2024-02-15) URLs are:

- https://s01.oss.sonatype.org/content/repositories/snapshots
- https://s01.oss.sonatype.org/service/local/staging/deploy/maven2/

Next, we need a staging plugin to deploy the artifacts to the OSSRH staging repository. The plugin is configured as follows:
```XML
<plugin>
	<groupId>org.sonatype.plugins</groupId>
	<artifactId>nexus-staging-maven-plugin</artifactId>
	<version><latest version here></version>
	<extensions>true</extensions>
	<configuration>
		<serverId>ossrh</serverId>
		<nexusUrl><REPO ROOT URL></nexusUrl>
		<autoReleaseAfterClose>true</autoReleaseAfterClose>
	</configuration>
</plugin>
```
Here, the `<REPO ROOT URL>` is the root URL of the repositories above, e.g., for recent versions, it is `https://s01.oss.sonatype.org/`.


#### Setting up user authentication for the OSSRH
The following configuration must be present in the `settings.xml` file:
```XML
<servers>
	<server>
		<id>ossrh</id>
		<username>your username</username>
		<password>your password</password>
	</server>
</servers>
```


# Profiles
Maven profiles can be used to supply different configurations in a single `pom.xml` file. This can be used for example to:

- support different build environments (e.g., development, testing, production)
- support different build targets (e.g., different Java versions)
- support different build configurations (e.g., optional dependencies)

Profiles are defined in the `profiles` section of the `pom.xml` file. Each profile has a unique id and can contain any configuration that can be present in the `pom.xml` file. 

To manually activate a profile, we can use the `-P` argument of the `mvn` command:
```
mvn <goal> -P <profile id>
```

Note that **the profile needs to be selected for all relevant goals, not just for the compilation**. For example, if we have and optional dependency in the profile, we need to select the profile for `compile`, but also for `exec`, `install`, etc, otherwise the dependency will not be found at runtime.

## Displaying active profiles
To display the active profiles, use the following command:
```
mvn help:active-profiles
```

Note that again, this will only show the profiles that are activated in the `settings.xml` file or the profiles that are activated by default. To test an optional profile, we need to activate it even for the `help:active-profiles` goal:
```
mvn help:active-profiles -P <profile id>
```


# Creating maven plugins

[Official guide](https://maven.apache.org/guides/plugin/guide-java-plugin-development.html)

Maven plugins can be created as maven projects. Specifics `pom` configuration:

- The packaging is `maven-plugin`
- The name of the plugin is `<artifactId>-maven-plugin`
- among the dependencies, there should be `maven-plugin-api` and `maven-plugin-annotations`

To use a cclass method as an entry point for a plugin goal, we annotate it with `@Mojo(name = "<goal name>")`.


## Testing a maven plugin
The best way to test the plugin is to run it separately, even if it should be later bound to a lifecycle phase. To run the plugin, we use the following syntax:
```
mvn <group id>:<artifact id>:<goal name>
# Example:
mvn com.test:example-maven-plugin:example
```

This is indeed very verbose. To shorten it, we can add a special configuration to the system `settings.xml` file:
```XML
<pluginGroups>
	<pluginGroup>com.test</pluginGroup>
</pluginGroups>
```
Now, we can run the plugin using:
```
mvn example:example
```


## Debugging a maven plugin in IntelliJ IDEA
Maven plugins can be easily debugged in IntelliJ IDEA. However, it is important to understand that unlike maven plugins are run from the local repository, not from the project source code. Therefore, **we need to install the plugin after each change**.


## Make the plugin runnable from any directory
Normally, the goals can be run only from project directories (where the `pom.xml` is present). To make the plugin runnable from any directory, we need to annotate the goal with `@requiresProject = false`:
```Java
@Mojo(name = "example", requiresProject = false)
```


# Various useful tasks
## Displaying the classpath
To display the classpath, use the following command:
```
mvn dependency:build-classpath
```
