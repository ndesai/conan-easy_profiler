from conans import ConanFile, CMake, tools


class EasyprofilerConan(ConanFile):
    name = "easy_profiler"
    version = "2.0.1"
    license = "https://github.com/yse/easy_profiler/blob/develop/LICENSE"
    author = "https://github.com/yse/easy_profiler/graphs/contributors"
    url = "https://githost.nevint.com/skywalker/utilities/conan-easy_profiler"
    description = "Lightweight cross-platform profiler library for c++"
    topics = ("easy_profiler", "profiling", "C++", "profiler")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [ True, False ],
        "fPIC": [ True, False ],
        "enable_samples": [ True, False ],
        "enable_gui" : [ True, False ]
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'enable_samples': False,
        'enable_gui': False
    }
    generators = "cmake"
    source_subfolder = "source_subfolder"

    # Custom variables
    source_url = "https://github.com/ndesai/easy_profiler.git"
    source_branch = "feature/qnx-support"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        self.run("git clone %s %s" % (self.source_url, self.name))
        self.run("cd %s && git checkout %s" % (self.name, self.source_branch))

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["EASY_PROFILER_NO_SAMPLES"] = not self.options.enable_samples
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["EASY_PROFILER_NO_GUI"] = not self.options.enable_gui
        cmake.configure(source_folder=self.name)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(['psapi', 'ws2_32'])
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['anl', 'pthread'])
        elif self.settings.os == "QNX":
            self.cpp_info.libs.extend(['socket'])
            