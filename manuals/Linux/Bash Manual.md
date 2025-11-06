# Bash Manual

[documentation](https://www.gnu.org/software/bash/manual/bash.html)

[wiki](https://en.wikipedia.org/wiki/Bash_(Unix_shell))

Bash can refer to a typical Unix shell, or just the command line interpreter for this shell or to the language used to write shell commands and scripts.

In bash, **commands can be separated** by

- a newline, or
- a semicolon.

Therefore, we can write even complicated commands to a single line in the terminal.


# General Remarks

- It's important to use Linux newlines, otherwise, bash scripts will fail with unexpected character error
- Empty constructs are not allowed, i.e, empty function or loop results in an error
- brackets needs spaces around them, otherwise, there will be a syntax error
- space around `=`, which is typical in other languages, is not allowed in bash 
- bash does not support any data structures, only arrays

# Bash modes and environment initialization
Bash can run in several modes. These modes have some effect, but mainly, it affects the initialization of the environment, i.e., which files are executed at the start of the shell. The modes are:

- **login shell**: mode is used when the user logs in. 
	- also used when the shell is run with the `-l`, `--login` parameter
- **interactive shell**: mode is used when the user interacts with the shell.
	- also used when the shell is run with the `-i` parameter
- **non-interactive shell**: mode is used when the shell is run in a script.
	- this shell mode is used when we run commands over ssh or wsl

The execution of the initialization files is displayed in the image below:

![Bash initialization files](Bash%20environment%20loading.png)

Note that the initialized environment persists in the system. In other words, the environment variables set in the files processed by the login shell are available even in the non-interactive non-login shells opened later on. However, there are still cases when the environment variables are not available because the login shell has not been run, e.g.:

- when the shell is run over ssh as a command: `ssh user@host <command>`
- when the shell is run from wsl as a command: `wsl <command>`

In those cases, if we need the environment variables, we have to run the login or interactive shell explicitly, e.g.: `wsl bash -lc <command>`.

# Variables
Variables can be defined as:
```bash
var=value
```
Note that **there must not be any spaces around `=`**. 

We can also declare variables with a specific type, so that no other type can be assigned to it using the `declare` command:
```bash
declare -i var # integer
declare -a var # array
declare -r var # read only
```

To access the value of a variable, we use `$`:
```bash
echo $var
```

## Assigning the output of a command to a variable
The output of a command can be assigned to a variable only with the [command substitution](#command-substitution):
```bash
var=<command> # wrong, the first token of the command is assigned to the variable

var=$(<command>) # correct, the output of the command is assigned to the variable
```

Example:
```bash
var=$(echo $var | sed 's/old/new/')
```





## List all variables
To list all variables, we can use the declare command:
```bash
declare
```
However, this command also lists the functions. To list only the variables, we can use:
```bash
declare -p
```
which also prints the type and attributes of the variables.

## Operations on variables
There are many operations on variables, the most important are:

- `${#<variable>}`: length of the variable
- `${<variable>%%<pattern>}`: remove the longest suffix matching the pattern
- `${<variable>##<pattern>}`: remove the longest prefix matching the pattern



# Working with I/O

## Output Forwarding
Output forwarding is a process of redirecting the output of a command to an input of another command. The operator for that is the pipe `|`. The syntax is:
```bash
<command 1> | <command 2>
```

Note that the content of the pipe cannot be examined, the process on the right hand side consume it. Therefore, **it is not possible to simply branch on pipe content** while use it in the subsequent process.


## Output Redirection
Output redirection is a process of redirecting the output (stdout, stderr,..) from the console to a file. The syntax is:
```bash
<command> <operator> <file>
```
The possible operators and their effects are listed in the table (full explanation on [SO](https://askubuntu.com/a/731237/603617)) below:

| Operator | Stdout | Stderr | Mode (in file) | 
| --- | --- | --- | --- |
| `>` | file | console | overwrite |
| `>>` | file | console | append |
| `&>` | file | file | overwrite |
| `&>>` | file | file | append |
| `2>` | console | file | overwrite |
| `2>>` | console | file | append |
| `\| tee` | both | console | overwrite |
| `\| tee -a` | both | console | append |
| `\|& tee` | both | both | overwrite |
| `\|& tee -a` | both | both | append | 

`tee` is actully a command, not an operator. It is used as follows:
```bash
<command> | tee <file>
```

We can also use `tee` to forward the output of a command to multiple commands:
```bash
<command 1> | tee >(<command 2>) | <command 3>
```
This forward `<command 1>` to both `<command 2>` and `<command 3>`.

## Use bash variables as input
Bash variables can be used as input of a command. Syntax:
```bash
<command> <<< $<variable>` 
```


## Output and input redirection with `sudo`
We need to consider that the `sudo` command is not applied to the redirected input or output. Example:
```bash
sudo <command> > <file>
```
In the above command, the `sudo` command is applied to the `<command>`, but not to the file writing, which is a bash construct. Therefore, the command will fail if the file writing requires root access. The same goes for the input redirection if we need root access for reading a file.

The solution is to use `tee`:
```bash
sudo <command> | tee <file>
```


# Command Substitution
When we need to use an output of a command instead of a constant or variable, we have to use command substtution:
```bash
`<command>`
# or equivalently
$(<command>)
```
e.g.:
```bash
echo resut is: `cut -d, -f 7`
# or equivalently
echo resut is: $(cut -d, -f 7)
```




# Conditions
In general, condition in bash has the following syntax:
```bash
if <condition> 
	then <command>
	else <command>
fi
```

The condition can have several formats:

- **plain command**: the condition is true if the command returns 0
	```bash
	if grep -q "$text" $file 
		then ...
	fi
	```

- **`[ <condition> ] or test <condition>`**: The standard POSIX test construct. Now only suitable if we want to run the script outside bash.
	```bash
	if [ $var = 1 ]
	then ...
	fi
	```

- **`[[ <condition> ]]`**: The extended test construct. This is the recommended way of writing conditions, due to [several practical features](https://stackoverflow.com/questions/3427872/whats-the-difference-between-and-in-bash) (e.g., no need to quote variables, regex support, logical operators, etc.).
	```bash
	if [[ $var = 1 ]]
	then ...
	fi
	```

- **`(( <condition> ))`**: The arithmetic test construct. This is used for arithmetic conditions.
	```bash
	if (( $var == 1 ))
	then ...
	fi
	```

Note that if we want to use some arbitrary value (e. g. the *return value* of a command), or comparisons in the condition (similar to programming languages), we have to use one of the test constructs. 


**Mind the spaces around the braces!**

## String comparison
Strings can be compared using the standard `=` operator or the `==` operator. 

If we use the `[ ]` construct, we have to quote the variables, otherwise, the script will fail on empty strings or strings containing spaces:
```bash
if [ "$var" = "string" ]
then ...
fi

# or equivalently
if [[ $var = "string" ]]
then ...
fi
```


# Loops
The syntax of the loop is:
```bash
while <condition>
do
   <command1>
   <command2>
   ...
done
```

## Forward to loop
We can forward an input into while loop using `|` as usuall. Additionally, it is possible to read from file directly by adding `<` to the end like this:
```bash
while condition
do
   <command1>
   <command2>
   ...
done < <input>
```

The same goes for the output, i.e., we can forward th outut of a loop with `|`.


# Strings literals
String literals can be easily defined as:
```bash
str="string literal"
# or equivalently
str='string literal'
```
If we use double quotes, the variables are expanded, e.g., `echo "Hello $USER"` will print `Hello <username>`.

The problem arises when we want to use double quotes in the string literal containing variables, e.g., `normal string "quotted string" $myvar`. In this case, we have to use quite cumbersome syntax:
```bash
a = "normal string "\""quotted string"\""
# or equivalently
a = "normal string "'"'"quotted string"'"'
```

## Multiline string literals
There is no dedicated syntax for multiline string literals. However, we can use the *here document* syntax:
```bash
<target> << <delimiter> <content> 
<delimiter>
```

For example, to store the command in a variable, we can use:
```bash
db_sql = $(cat << SQL
CREATE DATABASE test_$name OWNER $name;
grant all privileges on database test_$name to $name;
SQL)
```
Note that the `<delimiter>` must be at the beginning of the line, otherwise, it will not work.

# Functions
Functions are defined as:
```bash
function_name() {
	<command 1>
	<command 2>
	...
}
```
For access the arguments of the function, we use the same syntax as for the script arguments (e.g., `$1` for the first argument).

We can create local variables in the function using the `local` keyword:
```bash
function_name() {
	local var1="value"
	...
}
```


# Reading from command line
To read from command line, we can use the `read` command. The syntax is:
```bash
read <variable>
```
where `<variable>` is the name of the variable to store the input. Important parameters:

- `-p <prompt>`: prints	the `<prompt>` before reading the input
- `-s`: do not echo the input (usefull for passwords)


# Bash Scripts

## Bash Script Arguments
We refer the arguments of a bash script as

- `$0` - the name of the script
- `$1..$n` - the arguments of the script
- `$@` - all the arguments of the script

Sometimes, it is useful to throw away processed arguments. This can be done using the `shift` command `shift <n>`, where `<n>` is the number of arguments to be thrown away (default is 1). The remaining arguments are then shifted to the left, i.e., `$2` becomes `$1` and so on.


## Bash Script Header Content
Usually, here are some special lines at the beginning of the bash script.

First, we can specify the interpreter to be used:
```bash
#!/bin/bash
```

Then we can set some flags for the script
```bash
set -<flags>
```

Useful flags are:

- `e`: exit on error
- `u`: error raised on undefined variables
- `o`: any command that returns a non-zero exit code will raise an error even when piped to another command

[detailed description gist](https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425?permalink_comment_id=3939684)


## Calling a script from another script in the same directory
To call a script *b* from script *a* in the same directory, it is not wise to use the relative path, it is evaluated from the current directory, not from the directory of the script. To be sure that we can call script *a* from anywhere, we need to change the working directory to the directory of the scripts first:
```bash
cd "$(dirname "$0")"
./B.sh
```

