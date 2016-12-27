# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/pbPlist
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of Samantha Marshall nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
require 'fileutils'
require 'rbconfig'

class CheckCommand
	def initialize(name)
		@name = name
		@exec = ""
	end
	attr_reader :name
	attr_accessor :exec
end

def get_envar(variable_name)
	if not ENV[variable_name]
		abort("Please set the environment varaible '#{variable_name}' to the correct value!'")
	end
	return ENV[variable_name]
end

module_name = "pbPlist"

install_record = "installed_files.txt"
lint_record = "lint_output.txt"

command_python2 = CheckCommand.new("python")
command_python3 = CheckCommand.new("python3")
command_pylint = CheckCommand.new("pylint")
command_tox = CheckCommand.new("tox")
command_coverage = CheckCommand.new("coverage")
command_ccreporter = CheckCommand.new("codeclimate-test-reporter")
command_gem = CheckCommand.new("gem")
command_pip2 = CheckCommand.new("pip")
command_pip3 = CheckCommand.new("pip3")
command_bundler = CheckCommand.new("bundle")


task :check do
    commands = [
        command_python2,
        command_python3,
        command_pylint,
        command_tox,
        command_coverage,
        command_ccreporter,
        command_gem,
        command_pip2,
        command_pip3,
        command_bundler,
    ]
    for command in commands do
        path = `command -v #{command.name} 2> /dev/null`
        if path == ""
        	abort("Could not find '#{command.name}', please ensure it is installed and in your $PATH")
        else
        	command.exec = path.strip
        	puts "#{command.name}... #{command.exec}"
        end
    end
end

desc "clean the previous installation"
task :clean do
    puts "Removing existing installation..."

    # ensure that the "installed_files.txt" record file exists, then reach each line as a path
    ## and then delete that file path
    ## 
    ## TODO: this doesn't solve the problem of leaving the .egg directory in place, which causes
    ## problems with resolving the installed path
    FileUtils.touch("#{install_record}")
    File.readlines("#{install_record}").each {|path| FileUtils.rm_rf(path)}
     
    FileList[
        "build/**/*", 
        "build/**", 
        "build/"
    ].each {|path| FileUtils.rm_rf(path)}

    FileList[
        "dist/**/*", 
        "dist/**", 
        "dist/"
    ].each {|path| FileUtils.rm_rf(path)}

    FileList[
        ".tox/**/*", 
        ".tox/**", 
        ".tox/"
    ].each {|path| FileUtils.rm_rf(path)}

    FileList[
        "htmlcov/**/*", 
        "htmlcov/**", 
        "htmlcov/"
    ].each {|path| FileUtils.rm_rf(path)}

    FileList[
        ".eggs/**/*", 
        ".eggs/**", 
        ".eggs/"
    ].each {|path| FileUtils.rm_rf(path)}

    FileList[
        "*.egg-info/**/*", 
        "*.egg-info/**", 
        "*.egg-info/"
    ].each {|path| FileUtils.rm_rf(path)}

    FileList[
        "**/.DS_Store"
    ].each {|path| FileUtils.rm_rf(path)}

    FileList[
        "**/*.pyc"
    ].each {|path| FileUtils.rm_rf(path)}

    FileList[
        "**/__pycache__/"
    ].each {|path| FileUtils.rm_rf(path)}
end

desc "build the library, this takes an optional argument 'python2' or 'python3' to specify the language target, default is 'python2'."
task :build, [:variant] => [:clean, :check] do |t, args|
    args.with_defaults(:variant => "python2")

    if args.variant == "python2"
        sh "#{command_python2.exec} setup.py install --record #{install_record}"
    elsif args.variant == "python3"
        sh "#{command_python3.exec} setup.py install --record #{install_record}"
    else
        abort("Please specify either 'python2' or 'python3' as the build target!")
    end
end

desc "runs the unit tests"
task :test => [:check] do
    sh "#{command_tox.exec}"
end

desc "runs the linter over the code"
task :lint => [:check] do
    FileUtils.touch("#{lint_record}")
    sh "#{command_pylint.exec} --rcfile=pylintrc #{module_name} > #{lint_record} || :"
end

namespace :reporter do
	task :coverage do
		sh "#{command_coverage.exec} report"
		sh "#{command_coverage.exec} html"
	end

	task :codeclimate do
		ccr_token = get_envar("CIRCLECI_CODECLIMATE_TOKEN")
		sh "#{command_ccreporter.exec} --token #{ccr_token}"
	end
end
task :report => [:check] do
	if not File.exist?(".coverage")
		abort("Please run 'rake test' prior to running 'rake report'")
	end
	Rake::Task["reporter:coverage"].invoke
	Rake::Task["reporter:codeclimate"].invoke
end

task :danger => [:check] do
	if ENV["DANGER_GITHUB_API_TOKEN"]
		danger_token = get_envar("DANGER_GITHUB_API_TOKEN")
		sh "#{command_bundler.exec} exec danger --verbose"
	else
		sh "#{command_bundler.exec} exec danger local --verbose"
	end
end

task :setup do
	user_flag = ""
	if RbConfig::CONFIG["host_os"].include? "darwin"
		user_flag = "--user"
	end
	sh "#{command_gem.name} install bundler #{user_flag}"
	sh "#{command_bundler.name} install"
	
	sh "#{command_pip2.name} install --requirement install_requirements.txt"
end

task :ci => [:setup, :check,  :lint, :test, :report, :danger] do
	if ENV["CIRCLE_ARTIFACTS"]
		FileUtils.cp_r("htmlcov/", ENV["CIRCLE_ARTIFACTS"])
		FileUtils.cp_r("#{lint_record}", ENV["CIRCLE_ARTIFACTS"])
	end
end

