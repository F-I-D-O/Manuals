# STL and Other Libraries Tools

# IO and Filesystem
The simple way to print to standard input is:
```cpp
std::cout << "Hello world" << std::endl;
```

To return to the begining of the line and overwrite the previous output, we can use the `'\r'` character:
```cpp
std::cout << "Hello world" << '\r' << std::flush;
```


## File path manipulation
Although we can use strings to work with file paths in C++, the standard format which is also easy to use is [`std::filesystem::path`](https://en.cppreference.com/w/cpp/filesystem/path) from the [filesystem library](https://en.cppreference.com/w/cpp/filesystem).

Basic operations:

- To **create a path**, we jusct call `std::filesystem::path(<string path>)`.
- We can easily **join two paths** by `auto full_path = <path 1> / <path 2>`;
- To get the **asolute path**, we call
	- [`std::filesystem::absolute(<path>)`](https://en.cppreference.com/w/cpp/filesystem/absolute) to get the path as `CWD/<path>`
	- [`std::filesystem::canonical(<path>)`](https://en.cppreference.com/w/cpp/filesystem/canonical) to get the dots resolved. Note that this method throws exception if the path does not exists.
- The path to the **current working directory** can be obtained by calling `std::filesystem::current_path()` and set using `std::filesystem::current_path(<path>)`.
- To change the file extension (in the C++ representation, not in the filesystem), we can call the [`replace_extension`](https://en.cppreference.com/w/cpp/filesystem/path/replace_extension) method.



## Filesystem manipulation
[cppreference](https://en.cppreference.com/w/cpp/filesystem) 

### Copying
To copy, we can use [`std::filesystem::copy(<source path>, <destination path>[, <options>])`](https://en.cppreference.com/w/cpp/filesystem/copy) function.

The options parameter type is [`std::filesystem::copy_options`](https://en.cppreference.com/w/cpp/filesystem/copy_options). This enum is a bitmask type, therefore, multiple options can be combined using the `|` operator. Example:
```cpp
auto options = std::filesystem::copy_options::recursive | std::filesystem::copy_options::overwrite_existing;

std::filesystem::copy("C:/temp/data", "c:/data/new", options);
```

Note that **unlike the unix `cp` command, the `copy` function does not copy the directoy itself**, even if the destination directory exists. Suppose we have two direcories:

- `C:/temp/new` 
- `C:/data/`

And we want to copy the `new` folder, so that the result is: `C:/data/new/`. In bash, this will be:
```bash
cp -r C:/temp/new C:/data/
```
While in C++, we need to do:
```cpp
std::filesystem::copy("C:/temp/new", "C:/data/new",  std::filesystem::copy_options::recursive);
```


### Creating directories
To create a directory, we can use [`std::filesystem::create_directory(<path>)`](https://en.cppreference.com/w/cpp/filesystem/create_directory) function. 

This function fails if the parent directory does not exist. To create the parent directories as well, we can use [`std::filesystem::create_directories(<path>)`](https://en.cppreference.com/w/cpp/filesystem/create_directory) function.


### Removing files and directories
To remove a file or an empty directory, we can use [`std::filesystem::remove(<path>)`](https://en.cppreference.com/w/cpp/filesystem/remove) function.

To remove a content of a directory we can use `std::filesystem::remove_all(<path>)` function listed on the same page of cppreference.


### Other useful functions

- [`std::filesystem::exists(<path>)`](https://en.cppreference.com/w/cpp/filesystem/exists)
- [`std::filesystem::is_directory(<path>)`](https://en.cppreference.com/w/cpp/filesystem/is_directory)
- [`std::filesystem::is_regular_file(<path>)`](https://en.cppreference.com/w/cpp/filesystem/is_regular_file)
- [`std::filesystem::is_empty(<path>)`](https://en.cppreference.com/w/cpp/filesystem/is_empty)


### Getting a temporary folder
To get a temporary folder, we can use the [`std::filesystem::temp_directory_path`](https://en.cppreference.com/w/cpp/filesystem/temp_directory_path) function.


## Manual text IO

### Input
For input, we can use [`std::ifstream`](https://en.cppreference.com/w/cpp/io/basic_ifstream):
```cpp
std::ifstream file;
file.open(<path>);
...
file.close();
```
The important thing is that we need to check whether the `open` call was successful. **The `open` function never throws an exception, even if the file does not exist**, which is a common case. Instead, it only sets the `failbit` of the stream. Without some check, the failure is hidden as an ifstream  in a fail state behaves as if it was empty.

For reading **line by line**, we can use the `std::getline` function:
```cpp
std::string line;
while (std::getline(file, line)) {
	// do something with the line
}
```

However, processing the line is currently not very convenient in C++ because functions from other languages like `split` are missing.

For **reading whitespace delimited tokens** we can instead use the [`>>` operator](https://en.cppreference.com/w/cpp/io/basic_istream/operator_gtgt) on the stream:
```cpp
// file content: "01 Smith"

int id;
std::string name;

file >> id >> name;
```

If we need to skip some tokens, its best to introduce a dummy string variable:
```cpp
// file content: "01 2021-01-01 active Smith"

int id;
std::string dummy;
std::string name;

file >> id >> dummy >> dummy >> name;
```

Conveniently, the input streams have a `bool` operator that states whether the stream is in a state ready for reading. This way, we can easily stop the loop when the file is read, because the `>>` operator returns the stream itself:
```cpp
// read the whole file
while (file >> id >> name) {
	...
}
```





### Output
For line by line output, we use `std::ofstream`:
```cpp
std::ofstream file;
file.open(<path>);
batch_file << "first line" << std::endl;
batch_file << "second line" << std::endl;
...
batch_file.close();
```


## Load whole file into string
Again, we use the `std::ifstream`, but this time, we also use the `std::istreambuf_iterator` to read the whole file into a string:
```cpp
std::ifstream file(<path>);
std::string content(std::istreambuf_iterator<char>{file}, {});
```
Here, the `std::istreambuf_iterator<char>` is created using initialization instead of the constructor so that the local variable is not confused with function declaration. The `{}` is used to create an empty string, which is the end of the range for the iterator.

## csv
### Input
### Output
For csv output, we can usually use the general line-by-line approach.


## YAML
For YAML, we can use the [yaml-cpp](https://github.com/jbeder/yaml-cpp/) library. We can load

- from file using `YAML::LoadFile(<path>)`
- from string using `YAML::Load(<string>)`
	- for some reason, the `YAML::Load` function does not work with objects separated by indentation, so we need to use `{}` to separate the objects. 

To test whether a `YAML::Node` **contains a certain key**, we may use the `[]` operator, as it does not create a new node (unlike the stl containers):
```cpp
YAML::Node node;
if (node["key"]) {
	// do something
}
```
The **iteration** over the keys is done using `YAML::const_iterator`:
```cpp
for (YAML::const_iterator it = node.begin(); it != node.end(); ++it) {
	std::string key = it->first.as<std::string>();
	YAML::Node value = it->second;
}
```

To **check the type of a node**, we can use the `Type()` method. The possible types are:

- `NodeType::Null`
- `NodeType::Scalar`
- `NodeType::Sequence`
- `NodeType::Map`
- `NodeType::Undefined`

To **get the value of a node**, we can use the `as<T>()` method, where `T` is the type of the value we want to get. Unfortunately, there is no way to check if the conversion is possible. The solution for cases with multiple supported types in a single node is to use exceptions as control statements:

```cpp
try {
	int value = node.as<int>();
} catch (const YAML::BadConversion& e) {
	std::string string_value = node.as<std::string>();
    ...
}
```




## HDF

To load data from HDF5 files, the HDF5 C++ API can be used. Typical usage:

```cpp
#include <H5Cpp.h>

const H5::H5File file("file.h5", H5F_ACC_RDONLY);

const H5::DataSet dataset = file.openDataSet("dataset");
const H5::DataSpace dataspace = dataset.getSpace();
hsize_t dims[2];
dataspace.getSimpleExtentDims(dims);
H5::DataSpace memspace(2, dims);

dataset.read(
	<pointer where to store the data>,
	H5::PredType::<data type>,
	memspace,
	dataspace
);
```

If we do not know the dataset name, we can get the name by index:
```cpp
std::string dataset_name = file.getObjnameByIdx(0); // get the first dataset name
```

To check if the dataset exists, we can use the `exists` method of the file:
```cpp
const H5::H5File file("file.h5", H5F_ACC_RDONLY);
if (file.exists("dataset")) {
	...
}
```



# Iterators, STL algorithms, and ranges
If we want to iterate over elements in some programming language, we need to fulfill some interface. In Java, this interface is called `Iterable`. Also, there is usually some interface that formalize the underlying work, in Java, for example, it is called `Iterator`. 

In C++, however, the interface for iteration is not handled by polymorphism. Instead, it is handled using type traits and concepts. On top of that, there are multiple interfaces for iteration:

- legacy iteration, e.g., `for (auto it = v.begin(); it != v.end(); ++it)`
- STL algorithms, e.g., `std::find(v.begin(), v.end(), 42)`
- STL range algorithms, e.g., `std::ranges::find(v, 42)`
- STL range views, e.g., `std::ranges::views::filter(v, [](int x){return x > 0;})`

The following table summarizes the differences between the interfaces:
|---| Plain iteration | STL algorithms | STL range algorithms | STL range views |
|---|---|---|---|---|
| **Interface** | type traits | type traits | concepts | concepts |
| **Iteration** | eager | eager | eager | lazy |
| **Modify the underlying range*** | no | yes | yes | no |
| **Can work on temporaries** | yes | yes | yes | no |

*If the operation modifies the data, i.e., sorting, shuffling, transforming, etc.

The examples below demonstrate the differences between the interfaces on the following task: create a vector of 10 elements with values 0,1,2,...,9, i.e., the same as Python `range(10)`.
```cpp
// plain iteration
std::vector<int> vec(10);
int i = 0;
for (auto it = vec.begin(); it != vec.end(); ++it) {
	*it = i;
	++i;
}

// legacy algorithm
std::vector<int> vec(10);
std::iota(vec.begin(), vec.end(), 0); // C++11 way, legacy interface using type traits

// range algorithm
std::vector<int> vec(10);
std::ranges::iota(vec.begin(), vec.end(), 0); // basically the same, but the constructor arguments are constrained with concepts

// same using adaptor
auto range = std::views::iota(0, 10);
std::vector vec{range.begin(), range.end()}; // in-place vector construction
```


## Terminology 

- *range*: the object we iterate over (Iterable in Java)
- *iterator*: the object which does the real work (Iterator in Java)

Usually, a range is composed of two iterators:

- *begin*: points to the beginning of the range, returned by `<range_object>.begin()`
- *end*: points to the end of the object, returned by  `<range_object>.end()` 

Each iterator implements the dereference (`*`) operator that acces the element of the range the iterator is pointing to.

Depending on the iterator type, the iterator also supports other operations: `++`, `--` to iterate along the range, array index operator (`[]`) for random access, etc.

Most of the STL *collections* (vector, set,...) are also ranges.


## How to choose the correct interface?
when deciding which interface to use, we can use the following rules:

1. **If the number of tasks and the complexity of the tasks is high, use the legacy iteration**. It is hard to write a 20 line for loop with various function calls as algorithm or adaptor and the result would be hard to read.
1. Otherwise, **if you need to preserve the original range as it is or you need to compose multiple operations, use the STL range adaptors**. 
1. Otherwise, **use the STL range algorithms**.

Note that the in this guide, we do not consider the legacy STL algorithms. With the availability of the STL *range* algorithms, there is no reason to use the legacy algorithms, except for the backward compatibility or for the algorithms that are not yet implemented in the STL.

Also note that some STL algorithms are principially non-modifying, e.g., `std::ranges::find` or `std::ranges::count`. These algorithms logically do not have the adaptor equivalent.


## STL ranges and views
[https://en.cppreference.com/w/cpp/ranges](https://en.cppreference.com/w/cpp/ranges)

In C++ 20 there is a new range library that provides functional operations for iterators. It is similar to functional addon in Java 8.

As explained in the beginning of this chapter, there are two ways how to use the STL ranges:

- using the [range algorithms](https://en.cppreference.com/w/cpp/ranges) (`ranges::<alg name>`) that are invoked eagerly.
- using the [range views](https://en.cppreference.com/w/cpp/ranges/views) (`ranges::views::<view name>`) that are invoked lazily.

Note that the range algorithms and adaptors cannot produce result without an input, i.e., **we always need a range or collection on which we want to apply our algorithm/view.**

### STL range views
The difference of range view to range algorithms is that the views are lazy, i.e., they do not produce any result until they are iterated over. This is similar to the Python generators. The advantage is that we can chain multiple views together and the result is computed only when we iterate over the final view.

Note that due to the lazy nature of the views, **the underlying range has to be alive during the whole iteration**. Therefore, we cannot use the views on temporaries, e.g., we cannot useviews directly in the constructor of a vector, or we cannot use the views on a temporary range returned by a function.

A custom view can be created so that it can be chained with STL views. However, it has to satisfy the [view concept](https://en.cppreference.com/w/cpp/ranges/view), and more importantly, it should satisfy the view semantic, i.e., it should be cheap to copy and move (without copying the underlying data).

#### Usefull views

- [`std::views::iota`](https://en.cppreference.com/w/cpp/ranges/iota_view): generates a sequence of numbers
- [`std::views::filter`](https://en.cppreference.com/w/cpp/ranges/filter_view): filters the elements of the range


### Projections
Unlike in Java, we cannot refer to member functions when lambda functions are required. However, we can use these member functions when the algorithm or adaptor has a *projection* parameter. Example:
```cpp
struct Data {
	int a;
	std::string b;
	...
};

std::vector<Data> data = get_data();

std::sort(data, {}, &Data::b);
```
The trick here is that we can only provide the member that we want to use for sorting, but the sorting logic (`first < second`...) is handeled by a standard comparator (the second argument initialized with `{}`).

We can have even more complicated projections that are not just references to member functions:
```cpp
std::vector<My_class> objects = get_objects();
std::vector<unsigned> indexes = get_indexes(objects);
auto proj = [&objects](std::size_t i) -> const std::string& { 
	return objects[i].get_name(); 
};
std::ranges::sort(indexes, {}, proj) // sort indexes using the property of objects
```


### Useful range algorithms
Note that the most frequently used algorithms have a separate section in the Iterators chapter.

- [`std::shuffle`](https://en.cppreference.com/w/cpp/algorithm/random_shuffle) : shuffles the elements in the range (formerly `std::random_shuffle`).
- [`std::adjacent_find`](https://en.cppreference.com/w/cpp/algorithm/adjacent_find) : finds the first two adjacent elements that are equal. Can be used to find duplicates if the range is sorted.
- [`std::ranges::unique`](https://en.cppreference.com/w/cpp/ranges/unique): moves the duplicates to the end of the range and returns the iterator to the first duplicate. Only consecutive duplicates are found.
- [`std::ranges::min`](https://en.cppreference.com/w/cpp/algorithm/ranges/min) : finds the smallest element in the range. We can use either natural sorting, or a comparator, or a projection. If the range is empty, the behavior is undefined.
- [`std::ranges::min_element`](https://en.cppreference.com/w/cpp/algorithm/ranges/min_element) : finds the smallest element in the range. Unlike `std::ranges::min`, this function returns an iterator to the smallest element. 
- [`std::ranges::empty`](https://en.cppreference.com/w/cpp/algorithm/ranges/empty) : checks whether the range is empty. 


### Other Resources

-   [https://www.modernescpp.com/index.php/c-20-the-ranges-library](https://www.modernescpp.com/index.php/c-20-the-ranges-library) 



## Boost ranges
In addition to the STL range algorithms and adaptors, boost has it's own [range library](https://www.boost.org/doc/libs/1_80_0/libs/range/doc/html/index.html) with other more complex algorithms and adaptors.

### Boost range requirements
Sometimes, it is hard to say why a type does not satisfy some of the requirements for boos ranges. Fortunatelly, the boost provides concepts for checking whether a type satisfy each specific range model. Example:
```cpp
BOOST_CONCEPT_ASSERT((
	boost::SinglePassRangeConcept<std::vector<int>>
)); // true
```

Also, it is necessary to check whether the value of the iterator can be accessed:
```cpp
BOOST_CONCEPT_ASSERT((
	boost_concepts::ReadableIteratorConcept<
		typename boost::range_iterator<std::vector<int>>::type
	>
)); // true
```

Most likely, the compiler will complain that `boost::range_iterator<R>::type` does not exist for your range `R` . The boost range library generate this type by a macro from the `R::iterator` type. Therefore, make sure that your range has an iterator type defined, either as:

- a type alias to an existing iterator
- an iterator nested class
 
Note that **`<RANGE CLASS>::iterator` and `<RANGE CLASS>::const_iterator` has to be accessible (public).**

## Sequences
The `iota` algortihm/adapter is used to create a sequence:
```cpp
auto range = std::views::iota(0, 10);
auto vec = std::vector(range.begin(), range.end());
```
Note that we cannot pass the view directly to the vector, as the vector does not have a range constructor.

## Zip
The classical Python like zip iteration is available using the [zip adapator](https://en.cppreference.com/w/cpp/ranges/zip_view), which is not yet supported in MSVC.

However, boost provides a similar functionality `boost::combine`.

### `boost::combine`
[`boost::combine`](https://www.boost.org/doc/libs/1_80_0/libs/range/doc/html/range/reference/utilities/combine.html) example: 
```cpp
std::vector<int> va{1, 2, 3};
std::vectro<float> vb{0.5, 1, 1.5};
for(const auto& [a, b]: boost::combine(va, vb)){
	...
}
```
Each argument of combine must satisfy [boost::SinglePassRange](https://www.boost.org/doc/libs/1_80_0/libs/range/doc/html/range/concepts/single_pass_range.html)


## Enumerating
There is no function in standard library equivalent to the python enumerate. We can use a similar boost solution:
```cpp
#include <boost/range/adaptor/indexed.hpp>

for(auto const& el: <range> | boost::adaptors::indexed(0)){
	std::cout << el.index() << ": " << el.value() << std::endl;
}
```
However, inside the loop, we have to call the `index` and `value` functions, so it is probably easier to stick to the good old extra variable:
```cpp
size_t i = 0;
for(auto const& el: <range>) {
  std::cout << i << ": " << el << std::endl;
  ++i;
}
```


## Sorting
There is no sorted view or something simmiler, so in order to sort a range, we need to:

- really sort the object in the range
- create an adaptor/view from the range, and then sort the view

There are two functions for sorting in the STL algorithm library:

- [`std::sort`](https://en.cppreference.com/w/cpp/algorithm/sort): old
	- supports parallelization directly by the policy param
- [`std::ranges::sort`](https://en.cppreference.com/w/cpp/algorithm/ranges/sort): new
	- supports comparison using projections

There are three types of sorting:

- natural sorting using the `<` operator of `T` : `std::sort(<RANGE<T>>)`
- sorting using a comparator: `std::sort(<RANGE>, <COMPARATOR>)`, where comparator is a fuction with parameters and return value analogous to the natural sorting operator.
- sorting using projection (only availeble in `std::ranges::sort`): `std::ranges::sort(<RANGE>, <STANDARD GENERIC COMPARATOR>, <PROJECTION>`

### Sorting using projection
When we want to sort the objects by a single property different then natural sorting, the easiest way is to use projection. Example:
```cpp
struct Data {
	int a;
	std::string b;
	...
};

std::vector<Data> data = get_data();

std::sort(data, {}, &Data::b);
```
The trick here is that we can only provide the member that we want to use for sorting, but the sorting logic (`first < second`...) is handeled by a standard comparator (the second argument initialized with `{}`).

We can have even more complicated projections:
```cpp
std::vector<My_class> objects = get_objects();
std::vector<unsigned> indexes = get_indexes(objects);
auto proj = [&objects](std::size_t i) -> const std::string& { 
	return objects[i].get_name(); 
};
std::ranges::sort(indexes, {}, proj) // sort indexes using the property of objects
```


## Transformation
Transformation alg/views transforms an input range according to a callable. As with other operation, there are thre options:

- classical algorithm: [`std::transform`](https://en.cppreference.com/w/cpp/algorithm/transform) with a direct paralellization using the policy parameter
- range algorithm: [`std::ranges::transform`](https://en.cppreference.com/w/cpp/algorithm/ranges/transform) with a support for projections
- range view: [`std::ranges::views::transform`](https://en.cppreference.com/w/cpp/ranges/transform_view) - a lazy variant

The algorithms (but not the view) also supports **binary transformations**, i.e., create an output range using two input ranges.

Transform view example:
```c++
std::vector<int> in(3, 0); // [0, 0, 0]
auto ad = std::ranges::transform_view(in, [](const auto in){return in + 1;});
std::vector<int> out(ad.begin(), ad.end());
```

The transform *view*  can be only constructed from an object satisfying [`ranges::input_range`](http://en.cppreference.com/w/cpp/ranges/input_range). If we want to use a general range (e.g., vector), we need to call the addapter, which has a same signature like the view constructor itself. The important thing here is that the adapter return type is not a `std::ranges::views::transform<<RANGE>>` but `std::ranges::views::transform<std::ranges::ref_view<RANGE>>>` ([`std::ranges::ref_view`](https://en.cppreference.com/w/cpp/ranges/ref_view)). Supporting various collections is therefore possible only with teplates, but not with inheritance.

**Note that unlike in Java, it is not possible to use a member reference as a transformation function (e.g.: `&MyClass::to_sting()`).** We have to always use lambda functions, `std::bind` or similar to create the callable.


## Aggregating (sum, product, etc.)
These operations can be done using the [`std::accumulate`](https://en.cppreference.com/w/cpp/algorithm/accumulate) algorithm. This algorithm is about to be replaced by the `std::ranges::fold` algorithm, but it is not yet implemented in Clang. Examples:
```cpp
// default accumulation -> sum
std::vector<int> vec{1, 2, 3, 4, 5};
int sum = std::accumulate(vec.begin(), vec.end(), 0);

// product
int product = std::accumulate(vec.begin(), vec.end(), 1, std::multiplies<int>());
```


## Implementing a custom range
There are different requirements for different types of ranges. Moreover, there are different requirements for the [range-based for loop (for each)](https://en.cppreference.com/w/cpp/language/range-for), or the legacy STL algorithms. 

Here we focus on requirements for ranges. Not however, that the range requirements are more strict than the requirements for the range-based for loop or the legacy STL algorithms. Therefore, the described approach should work for all three cases.

Usually, we proceed as follows:

1. Choose the right range (Iterable) concept for your range from the [STL range concepts](https://en.cppreference.com/w/cpp/ranges).
	- The most common is the [`std::ranges::input_range`](https://en.cppreference.com/w/cpp/ranges/input_range) concept.
1. Implement the range concept for the range.
	- Either, we can do it by using the interface of the undelying range we usein our class (i.e, we just forward the calls to the methods of `std::vector` or `std::unordered_map`) or
	- implement the interface from scratch. For that, we also need to implement the iterator class that fulfills the corresponding [iterator concept](https://en.cppreference.com/w/cpp/iterator) (e.g., [`std::input_iterator`](https://en.cppreference.com/w/cpp/named_req/InputIterator) for the `std::ranges::input_range`).


### Implementing an input range
The input range is the most common range type. The only requirement for the input range is that it has to have the `begin` and `end` methods that return the input iterator. Example:
```cpp
class My_range {
	private:
		std::vector<int> data;
	public:
		My_range(std::vector<int> data): data(data) {}
		auto begin() {return data.begin();}
		auto end() {return data.end();}

		// usually, we also want a const version of the range
		auto begin() const {return data.begin();}
		auto end() const {return data.end();}
};
```

## Boost Iterator Templates
The [boost.iterator library](https://www.boost.org/doc/libs/1_77_0/libs/iterator/doc/index.html) provides some templates to implement iteratores easily, typically using some existing iterators and modifying just a small part of it:

- for pointer to type (dereference) iterator, you can use [boost indirect iterator](https://www.boost.org/doc/libs/1_54_0/libs/iterator/doc/indirect_iterator.html)
- [zip iterator](https://www.boost.org/doc/libs/1_80_0/libs/iterator/doc/zip_iterator.html) for Python like iteration over multiple collections
- [transform iteratorather useful iterators are also included in [the boost.iterator library](https://www.boost.org/doc/libs/1_787_0/libs/iterator/doc/transform_iterator.html) for using another iterator and just modify the access (`*`) opindex.html). including:
	- zip iterator.
	- [counting_iterator](https://live.boost.org/doc/libs/1_78_0/libs/iterator/doc/counting_iterator.html) to create number sequence like Python range
- [gentransform iterator](https://livewww.boost.org/doc/libs/1_787_0/libs/iterator/doc/generattransform_iterator.html)

There are also two general (most powerfull) classes:

- [iterator adapter](https://live.boost.org/doc/libs/1_78_0/libs/iterator/doc/iterator_adaptor.html)
- iterator facade


## Resources

-   [How to write a legacy iterator](https://internalpointers.com/post/writing-custom-iterators-modern-cpp)
    
-   [iter_value_t](https://en.cppreference.com/w/cpp/iterator/iter_t)



# Logging
There is no build in logging in C++. However, there are some libraries that can be used for logging. In this section we will present logging using the [spdlog](https://github.com/gabime/spdlog) library.

We can log using the `spdlog::<LEVEL>` functions:
```cpp
spdlog::info("Hello, {}!", "World");
```

By default, the log is written to console. In order to write also to a file, we need to create loggers manually and set the list of sinks as a default logger:
```cpp
const auto console_sink = std::make_shared<spdlog::sinks::stdout_sink_st>();
console_sink->set_level(spdlog::level::info); // log level for console sink

auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_st>(<log filepath>, true);

std::initializer_list<spdlog::sink_ptr> sink_list{console_sink, file_sink};
const auto logger = std::make_shared<spdlog::logger>(<LOGGER NAME>, sink_list);
logger->set_level(spdlog::level::debug); //log level for the whole logger

spdlog::set_default_logger(logger);
```

To save performance in case of an intensive logging, we can set an extended flushing period:
```cpp
spdlog::flush_every(std::chrono::seconds(5));
```

## Levels
The log levels are defined in the [`spdlog::level::level_enum`](https://github.com/gabime/spdlog/blob/v1.x/include/spdlog/common.h#L231). The levels are:

- `trace`
- `debug`
- `info`
- `warn`
- `error`
- `critical`

## Colors
By default, the logger uses colors for different log levels. However, this capability is lost when:

- using custom sinks or
- using custom formatters

To keep the colors, we need to a) use the color sink and b) explicitly set the usage of the color in the formatter:
```cpp
auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();

auto logger = std::make_shared<spdlog::logger>("console", console_sink);
logger->set_pattern("[%^%l%$] %v");
```
Here `%^` and `%$` are the color start and end markers.





# Testing with Google Test

## Private method testing
The testing of private method is not easy with Google Test, but that is common also for other test frameworks or even computer languages (see the common manual). Some solutions are described in [this SO question](https://stackoverflow.com/questions/47354280/what-is-the-best-way-of-testing-private-methods-with-googletest).

Usually, the easiest solution is to aplly some naming/namespace convention and make the function accessible.

For free functions:
```cpp
namespace internal {
	void private_function(){
		...
	}
}
```

For member functions:
```cpp
class MyClass{
public:
	void _private_function();
```


## Skipping a test
To set test to be skipped unless we mention it explicitly, we can use the `DISABLED_` prefix. Example:
```cpp
TEST(MyTest, DISABLED_test_name){
	...
}
```
This way, the test is skipped by default, but it can be run explicitly by mentioning it in the command line.


# Conditional Function Execution
W know it from other languages: if the function can be run in two (or more) modes, there is a function parameter that controls the execution. Usually, most of the function is the same (otherwise, we eould create multiple fuctions), and the switch controls just a small part.

Unlike in other langueges. C++ has not one, but three options how to implement this.  They are described below in atable together with theai properties.

| | function parameter | template parameter | compiler directive |
|--|--|--|--|
| good readability | yes| no |no | 
| compiler optimization | no | yes | yes |
| conditional code compilation | no | no | yes |

## Function Parameter
```cpp
void(bool switch = true){
	if(switch){
		...
	}
	else{
		...
	}
}
```

## Template Parameter
```cpp
template<bool S = true>
void(){
	if(S){
		...
	}
	else{
		...
	}
}
```

## Compiler Directive
```cpp
void(){
#ifdef SWITCH
    ...
#else
	...
#endif
}
```

# Ignoring warnings for specific line of code
Sometimes, we want to suppress some warnings, mostly in libraries we are including. The syntax is, unfortunatelly, different for each compiler. Example:
```cpp
#if defined(_MSC_VER)
	#pragma warning(push)
	#pragma warning(disable: <WARNING CODE>)
#elif defined(__GNUC__)
	#pragma GCC diagnostic push
	#pragma GCC diagnostic ignored "<WARNING TYPE GCC>"
#elif defined(__clang__)
	#pragma clang diagnostic push
	#pragma clang diagnostic ignored "<WARNING TYPE CLANG>"
#endif
.. affected code...
#if defined(_MSC_VER)
	#pragma warning(pop)
#elif defined(__GNUC__)
	#pragma GCC diagnostic pop
#elif defined(__clang__)
	#pragma clang diagnostic pop
#endif
```
Here, the `<WARNING CODE>` is the code of the warning to be suppressed without the `C` prefix.

**Note that warnings related to the preprocessor macros cannot be suppressed this way in GCC** due to a [bug](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53431) (fixed in GCC 13). The same is true for conditions:
```cpp
#if 0
	#pragma sdhdhs // unknown pragma raises warning, despite unreachcable
#endif
```

# Measuring used resource

## Memory

### MSVC
In MSVC, we can measure the peak used memory using the following code: 
```cpp
#include <psapi.h>

PROCESS_MEMORY_COUNTERS pmc;
K32GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc));
auto max_mem = pmc.PeakWorkingSetSize
```

# Working with tabular data
Potential libs similar to Python Pandas:

- [Arrow](https://arrow.apache.org/docs/cpp/)
- [Dataframe](https://github.com/hosseinmoein/DataFrame)


# Executing external commands
The support for executing external commands in C++ is unsatisfactory. The most common solution is to use the [`system`](https://en.cppreference.com/w/cpp/utility/program/system) function.
However, the `system` calls are not portable, e.g., the quotes around the command are not supported in Windows

Another option is to use the Boost [Process](https://www.boost.org/doc/libs/1_82_0/doc/html/process.html) library. 


# Command Line Interface
For CLI, please follow the [CLI manual](../Common.md#command-line-interface). Here we focus on setting up the [TCLAP](http://tclap.sourceforge.net/manual.html) library.

TCLAP use


# Jinja-like Templating
For working with Jinja-like templates, we can use the [Inja](https://github.com/pantor/inja) template engine. 


## Exceptions
There are the following exceptions types:

- `ParserError` thrown on `parse_template` method
- `RenderError` thrown on `write` method

### Render Errors

- `empty expression`: this signalize that some expression is empty. Unfortunatelly, the line number is incorrect (it is always 1). Look for empty conditions, loops, etc. (e.g., `{% if %}`, `{% for %}`, `{% else if %}`).



