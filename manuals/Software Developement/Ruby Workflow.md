Classical workflow is to use:

- [official Ruby distribution](https://www.ruby-lang.org/en/downloads/)
- [Bundler](https://bundler.io/) to manage dependencies

# Installation
## Windows

1. Download and run [Ruby installer](https://rubyinstaller.org/downloads/)
    - use the versin with DevKit
1. at the end, a command prompt will open, confitm the prompt with `Enter`


# Project setup
The project configuration is stored in the [*Gemfile*](https://bundler.io/v2.4/man/gemfile.5.html) file. It contains a list of dependencies, which are installed using the `bundle` command. Typically, the file contains the following lines:
```ruby
source "https://rubygems.org" # the source of the gems

gem "jekyll" # the gem to install
```

## Gems
Gems are packages for Ruby. They can be installed using the `gem` command, but moslty, they are installed as dependencies using the `bundle` command.  
The gem specification in the Gemfile contains the following parameters (split by spaces):

- **gem**: the name of the gem (required)
- **version**: the version of the gem
- **group**: the group of the gem. It can be used run a command only for a specific group. For example, `bundle install --without development` will not install gems from the `development` group.

The group parameter is a new syntax, the old syntax is to use the `group` command:
```ruby
group :development do
  gem "jekyll"
end
```