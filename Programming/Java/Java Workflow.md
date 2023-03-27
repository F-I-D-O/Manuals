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
-   Download maven from the official website and extract the archive somewhere (e.g. `C:/`)
-   Add absolute path to `<mavendir>/bin` to `PATH`

    
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
### Settings synchronization
1. Log in into JetBrains Toolbox or to the App
1. Click on the gear icon on the top-right and choose Sync
1. Check all categories and click on pull settings from the cloud
1. Resatart Ida to update all the settings

[More on Jetbrains](https://www.jetbrains.com/help/idea/sharing-your-ide-settings.html)

## Project configuration
The correct JDK has to be set up in various places:
- compielr has to be at least target jdk, set it in: `File` -> `Settings` -> `Build, Execution, Deployment` -> `Compiler` -> `Java Compiler` -> `Project bytecode version` and `Per-module bytecode version`
- language level should be the same as target jdk: `File` -> `Project Structure...` -> `Modules` -> `Language Level`
    

# Set Java version for project
There are two options to set:
- *source* version determines the least version of java that supports all language tools used in the source code. It is the least version that can be used to **compile** the source code.
- *target* version determines the least version of java that can be used to **run** your java application.

The target version can be higher than the source version, but not he other way around. most of the time, however, we use the same version for source and for target.

Usually, these versions needs to be set:
1. in the project compilation tool (maven) to configure the project compilation
2. in the IDE project properties, to configure the compilation of individual files, which is executed in the background to report the compilation errors at real time.

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

## Gurobi
Gurobi is a commercial project not contained in any public maven repositories. It is necessary to [install the gurobi maven artifact](http://fido.ninja/manuals/add-gurobi-java-interface-maven) manualy.

### Potential problems
- `unsatisfied linker error`: Check if the gurobi version in the error log matches the gurobi version installed.

# Archive

## AIC maven repo access

To Access the AIC maven repo, copy maven settings from another computer (located in ~/.m2)

> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEyMzk0MzE5ODgsODQ2NDIwNDY4LC0xNT
E3MzY3OTY5LDExMzQzNzcwNTcsLTczMDI5NjAyNyw3MzA5OTgx
MTZdfQ==
-->