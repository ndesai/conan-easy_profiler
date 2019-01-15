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
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    # Custom variables
    source_url = "https://github.com/ndesai/easy_profiler.git"
    source_branch = "feature/qnx-support"

    def source(self):
        self.run("git clone %s %s" % (self.source_url, self.name))
        self.run("cd %s && git checkout %s" % (self.name, self.source_branch))
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
#         tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)",
#                               '''PROJECT(MyHello)
# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.name)
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="easy_profiler/easy_profiler_core/include")
        # self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self.name]

