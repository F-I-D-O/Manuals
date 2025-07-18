# Java developement stack
We use this stack:

- Toolchain: JDK
- Package manager: standalone Maven
- IDE: Netbeans, Idea

# JDK
Java developem kit is the standard Java toolchain. Most comon tools are:

- `javac` for compilation
- `java` for execution


## [`javac`](https://docs.oracle.com/en/java/javase/12/tools/javac.html)
The syntax is:
```
javac [options] [sourcefiles]
```

## Warning control
By default, all warnings are disabled and only a summary of the warnings is displayed in the output (i.e., all warning types encountered, without specific lines where they occur).

To enable all warnings use the `-Xlint` argument. To enable/disable specific warnings, use `-Xlint:<warning name>` and `-Xlint:-<warning name>`, respectively.



# Maven
Described in the [Maven](./Maven.md) manual.

    
# Netbeans

-   Install the latest version of Apache Netbeans
-   Configuration:
	-   Autosaving: `Editor` -> `Autosave`
	-   Tab size, tabs instead of spaces, 120 char marker line: `Editor` -> `Formatting` -> `All Languages`
	-   Multi-row tabs: `Appearance` -> `DocumentTabs`
	-   Git labels on projects: `Team` -> `Versioning` -> `Show Versioning Labels`
	-   Internet Browser: `General` -> `web browser`
-   Javadoc config:
	-   if the javadoc for java SE does not work out of the box, maybe there is a wrong URL. Go to `Tools` -> `Java Platforms` -> `Javadoc` and enter there the path where the Javadoc is accessible online
-   Install the basic plugins
	-   [Markdown](https://github.com/madflow/flow-netbeans-markdown)

## Project configuration
### Configure Maven Goals
These can be configured in `Project properties` -> `Actions`

## Troubleshooting
If there is a serious problem, one way to solve it can be to delete the Netbeans cache located in `~\AppData\Local\NetBeans\Cache`.

# Idea
## Configuration
Configuration is done in `File` -> `Settings`. 

A lot of configuration we do in Idea Settings only applies to the current project. Therefore, it is a good idea to check whether the settings is not present in the template for new projects, so that we do not have to set it up for every new project. The settings template is located in `File` -> `New Project Setup`. 


### Settings synchronization

1. Log in into JetBrains Toolbox or to the App
1. Click on the gear icon on the top-right and choose Sync
1. Check all categories and click on pull settings from the cloud
1. Resatart Ida to update all the settings

[More on Jetbrains](https://www.jetbrains.com/help/idea/sharing-your-ide-settings.html)


### Maven configuration
By default, Idea uses the bundled Maven, which is almost never desired. It is best to swich to the system Maven, which we should done in:

- `File` -> `Settings` -> `Build, Execution, Deployment` -> `Build Tools` -> `Maven` -> `Maven home directory` for existing projects
- `File` -> `New Project Setup` -> `Maven` -> `Maven home directory` for new projects


### JDK configuration
The correct JDK has to be set up in various places:

- compielr has to be at least target jdk, set it in: `File` -> `Settings` -> `Build, Execution, Deployment` -> `Compiler` -> `Java Compiler` -> `Project bytecode version` and `Per-module bytecode version`
- language level should be the same as target jdk: `File` -> `Project Structure...` -> `Modules` -> `Language Level`
    

## Compilation
Everything is compiled in the background automatically. However, if we need to compile manually using maven, e.g., to activate certain plugins, we can compile using the maven tab on the right.


## Running Projects
To add or edit run configurations, click on the run configuration dropdown left of the run button and choose `Edit Configurations...`.

If the required configuration field is not present, it may be necessary to activate it by clicking on `Modify options` and choosing the desired option.


## Developing the whole project stack at once
If we are developing a whole stack of projects at once, it is best if we can navigate between them easily. However, it is not possible to open multiple projects in the same window in Idea (like in Netbeans). Instead, we need to open the project on the top of the stack and then add the other projects as modules. To add a module, click `File` -> `Project Structure` -> `Modules` and add the module.


## Running Maven Goals
Maven goals can be run from a dedicated tab on the right. The goals in the tab are divided into two categories:

- `Lifecycle` goals are the most common goals, which are used to build the project
- `Plugins` goals are the goals of the plugins used in the project

To run the goal, just double-click on it. 

If the run need some special configuration, right-click on the goal and choose `Modify Run Configuration...`

If the plugin is missing from the list, it may be necessary to reload the plugins. Click the `Reload All Maven Projects` button in the top left corner of the maven tab.

If the goal we want to run is neither a `Lifecycle` goal nor a `Plugin` goal (e.g., `exec`), we can run it by creating a run configuration and selecting maven type. Than, we select the maven goal by inserting it as a first argument in the `Command line` field.

### Maven goal configuration
To run a maven goal with a specific profile, add the profile name to the `Profiles` field.


## Troubleshooting

### Idea does not detect manually installed Maven artifact
Sometimes, idea cannot recognize installed maven artifact and marks it as missing (red). 

Fix: right click on the project or pom file -> `Maven` -> `Reload project`


### Idea does not see environment variables
These may be new environment variables, which were not present when Idea was started. Restart Idea to see the new environment variables.


### Idea does not set the correct classpath
Sometimes, Idea does not set the correct classpath for the project, and in consequence, there are errors reported in the editor, and the project fails to run (but compiles).

Solution: Invalidate the cache and restart Idea. This can be done by clicking `File` -> `Invalidate Caches / Restart...` -> `Invalidate and Restart`.


# Java version
[list of Java versions](https://en.wikipedia.org/wiki/Java_version_history)

There are multiple java versions to set:

- *source* version determines the least version of java that supports all language tools used in the source code. It is the least version that can be used to **compile** the source code.
- *target* version determines the least version of java that can be used to **run** your java application.
- *compile* version is the actual version used for compiling the code
- *runtime* version is the actual version used to run the Java program

The target version can be higher than the source version, but not he other way around. Most of the time, however, we use the same version for source and for target. The actual version used for compilation must be equal or higher than the source version. The actual version used for running the program must be equal or higher than the target version.

Usually, these versions needs to be set:

1. in the project compilation tool (maven) to configure the project maven compilation
2. in the IDE project properties to:
	- configure the compilation of individual files, which is executed in the background to report the compilation errors at real time.
	- configure the runtime environment for the program execution

Sometimes, the Java version used for running Maven has to be also set because it cannot be lower then the Java version used for project compilation using Maven.


[SO explanation](https://stackoverflow.com/questions/38882080/specifying-java-version-in-maven-differences-between-properties-and-compiler-p)


## Setting Java version in Maven
Since Java 9, both Java versions can be set at once with the release option:
```xml
<properties>
	<maven.compiler.release>10</maven.compiler.release>
</properties>
```
or equivalently
```xml
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-compiler-plugin</artifactId>
	<version>3.10.1</version>
	<configuration>
		<release>10</release>
	</configuration>
</plugin>
```

The old way is to use separate properties:
```xml
<properties>
	<maven.compiler.target>10</maven.compiler.target>
	<maven.compiler.source>10</maven.compiler.source>
</properties>	
```

**Note that the Java version configured in the pom file cannot be greater then the Java version used to run the Maven.**


## Setting Java version in Netbeans
**Note that for maven projects, this is automatically set to match the properties in the pom file.**

For the Netbeans real-time compiler, the cross compilation does not make sense, so both source and target Java version is set in one place: 

1. Right click on project -> `Properties` -> `Sources`
2. In the bottom, change the `Source/Binary Format`


## Setting Java version in IDEA
In idea, an extra step is sometimes necessary: to set the Java Language Level in the project settings: `File` -> `Project Structure...` -> `Modules` -> `Language Level`. The language level has to be lower or equal to the target version set in the maven configuration.


## Setting Java version used for executing Maven
If the Maven is executed from command line, edit the `JAVA_HOME` system property.

If the Maven is executed from Netbeans, edit `Project Properties` -> `Build` -> `Compile` -> `Java Platform`


## Enabling preview features
The preview features can be enabled using the `--enable-preview` argument. In Maven, this has to be passed to the compiler plugin:
```XML
<build>
	<plugins>
		<plugin>
			<artifactId>maven-compiler-plugin</artifactId>
			<version>3.8.0</version>
			<configuration>
				<enablePreview>true</enablePreview>
			</configuration>
		</plugin>
	</plugins>
</build>
```

For Maven compiler plugin older then version 3.10.1, use: 
```XML
<build>
	<plugins>
		<plugin>
			<artifactId>maven-compiler-plugin</artifactId>
			<version>3.8.0</version>
			<configuration>
				<compilerArgs>
					<arg>--enable-preview</arg>
				</compilerArgs>
			</configuration>
		</plugin>
	</plugins>
</build>
```

Unfortunatelly, it is also necessary to enable preview features in the IDE configuration: 

- In Netbeans, add `--enable-preview` to `Project Properties` -> `Run` -> `VM options`.
- In IDEA:
	1. add `--enable-preview` to `Settings` -> `Build, Execution, Deployment` -> `Compiler` -> `Java Compiler` -> `Override compiler parameters per-module`
	2. add `--enable-preview` to run configuration -> `Build and run` vm options


## Problems

### Runtime version error
A typical runtime version error is:
```
java.lang.UnsupportedClassVersionError: <executed class> has been compiled by a more recent version of the Java Runtime (class file version <higher version>), this version of the Java Runtime only recognizes class file versions up to <lower version>
```

First, we schould check the reported versions. There are two possible scenarios:

- The `<lower version>` is unexpectedly low. This means that we run the program with a lower version of JDK then the one we compiled it with. 
	- The solution is to set a different JDK to run the program.
- The `<higher version>` is unexpectedly high. This means that the class was compiled on some other machine, we have uninstalled the newest JDK, or we have set the wrong JDK in the compilation settings.  
	- The solution is to clean the project and recompile it. If it does not help, the problem can be in oneof the dependencies.
	
#### Check the version of java required at runtime	
There are various tactics, here listed from the easiest to the most universal:

- check the library documentation
- check the library `pom.xml` file
- check the `MANIFEST.MF` file in the library jar
- check the class file version using [javap](https://docs.oracle.com/en/java/javase/11/tools/javap.html): `javap -v <class file>`

# Gurobi
Gurobi is a commercial project not contained in any public maven repositories. It is necessary to [install the gurobi maven artifact](http://fido.ninja/manuals/add-gurobi-java-interface-maven) manualy.

## Potential problems

- `unsatisfied linker error`: Check if the gurobi version in the error log matches the gurobi version installed.


# Testing with JUnit
[homepage](https://junit.org/junit5/)

First, we need to add the JUnit dependency to `pom.xml`:
```xml
<dependency>
	<groupId>org.junit.jupiter</groupId>
	<artifactId>junit-jupiter</artifactId>
	<version><version></version>
	<scope>test</scope>
</dependency>
```

In test files, we just mark any test method with the `@Test` imorted as `org.junit.jupiter.api.Test`. Assertions are then imported statically from `org.junit.jupiter.api.Assertions`.



# Make part of the project optional
Sometimes we want to make a part of the project optional, so that it is not required at runtime or even at compile time. This is useful if that part of the project is:

- not essential for the project to work
- dependent on some external library, which can be cumbersome to install

The required steps are usually:

1. Create a maven profile for the optional part of the project
2. Move optional dependencies to the profile
3. Move optional source files outside the `src/main/java` directory
3. Use the `build-helper-maven-plugin` in the profile to add the optional source files to the project
4. At runtime, load the optional part of the project using the reflection

We now describe these steps in detail.

## Maven profiles and optional dependencies
A maven profile belongs to the `profiles` section of the `pom.xml` file. The structure is simple:
```xml
<profiles>
	<profile>
		<id>optional</id>
		<dependencies>
			<!-- optional dependencies -->
		</dependencies>
		<build>
			<plugins>
				<!-- optional plugins -->
			</plugins>
		</build>
	</profile>
```

## Moving optional source files outside the `src/main/java` directory
The optional source files can be moved anywhere, but a logical place is to create a new directory under `src/main`, e.g., `src/main/<lib>-optional`. 

Then we need to tell maven to include these files in the project if the optional profile is activated. This is done using the `build-helper-maven-plugin` in the optional profile:
```xml
<profiles>
	<profile>
		<id>optional</id>
		<build>
			<plugins>
				build-helper-maven-plugin here
			</plugins>
		</build>
	</profile>
</profiles>
```
For the `build-helper-maven-plugin` configuration, see the [Maven manual](Maven.md#using-dependencies-distributed-as-a-zip).


## Loading the optional part of the project at runtime
First, we should check if the optional part of the project is present at runtime:
```java
public static boolean libAvailable(){
	try {
		Class.forName("com.example.lib");
		return true;
	} catch (ClassNotFoundException e) {
		return false;
	}
}
```

Then, we can load the optional part of the project using reflection:
```java
if(libAvailable()){
	Class<?> libClass = Class.forName("com.example.lib");
	Object lib = libClass.newInstance();
	Method method = libClass.getMethod("someMethod");
	method.invoke(lib);
}
else{
	// handle missing library
}
```

# Archive

## AIC maven repo access

To Access the AIC maven repo, copy maven settings from another computer (located in ~/.m2)
