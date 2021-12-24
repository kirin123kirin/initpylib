cmake_minimum_required(VERSION 3.15)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 14)

## --- Please your setting --- #######################################
project(_PLEASE_PYPROJECT_NAME_ LANGUAGES CXX C)

set(EXENAME _PLEASE_EXECUTABLE_FILENAME_)

set(EXE_SOURCES _PLEASE_PYPROJECT_NAME_/main.cpp)

set(REAL_LIBNAME __PLEASE_PYPROJECT_NAME_)

set(LIBRARY_SOURCES _PLEASE_PYPROJECT_NAME_/${REAL_LIBNAME}.cxx)

#######################################################################

string(TOLOWER "${CMAKE_BUILD_TYPE}" _cmake_build_type)
if("${CMAKE_GENERATOR}" STREQUAL "Ninja" AND "${_cmake_build_type}" STREQUAL "pydebug")
    include("cmake/pydebug.cmake")
endif()

# print variables
macro(printvars)
    message(STATUS "\n\n*** dump start cmake variables ***\n\n")
    get_cmake_property(_variableNames VARIABLES)

    foreach(_variableName ${_variableNames})
            message(STATUS "${_variableName}=${${_variableName}}")
    endforeach()
    message(STATUS "\n*** dump end ***")
endmacro()

### if make executable file compile
IF (DEFINED EXENAME AND EXISTS EXE_SOURCES)
  add_executable(${EXENAME} ${EXE_SOURCES})
ENDIF()

### Example Depends On Include libxlsxwriter Project.
set(EXTERNAL_LIBBUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/external-build")
set(EXTERNAL_LIBRARY_PATH "${CMAKE_CURRENT_BINARY_DIR}/external-install")

    ### Create Target Dependency Library Project Build
    target_include_directories(${REAL_LIBNAME} PRIVATE ${EXTERNAL_LIBRARY_PATH}/include)
    target_link_directories(${REAL_LIBNAME} PRIVATE ${EXTERNAL_LIBRARY_PATH}/lib)

    find_library(xlsxwriter_LIBPATH xlsxwriter HINTS ${EXTERNAL_LIBRARY_PATH}/lib)
    find_library(zlibstatic_LIBPATH zlibstatic HINTS ${EXTERNAL_LIBRARY_PATH}/lib)

    if(xlsxwriter_LIBPATH AND zlibstatic_LIBPATH)
        target_link_libraries(${REAL_LIBNAME} LINK_PRIVATE xlsxwriter zlibstatic)
    
    else()

        ### zlib External static link
        target_link_libraries(${REAL_LIBNAME} zlibstatic)
        include(ExternalProject)

            ### https://runebook.dev/ja/docs/cmake/module/externalproject
            ExternalProject_Add(
                zlibstatic
                GIT_REPOSITORY https://github.com/madler/zlib.git
                GIT_TAG master
                PREFIX     ${EXTERNAL_LIBBUILD_DIR}
                CMAKE_GENERATOR "Ninja"
                CMAKE_ARGS
                    -DCMAKE_INSTALL_PREFIX=${EXTERNAL_LIBRARY_PATH}
                    -DCMAKE_BUILD_TYPE=Release
                # CONFIGURE_COMMAND "./configure --prefix=${EXTERNAL_LIBRARY_PATH}"
                # BUILD_COMMAND     "make"
                # INSTALL_COMMAND   "make install"
                # TEST_COMMAND      "make test"
            )

        ### xlsxwriter External static link
        target_link_libraries(${REAL_LIBNAME} xlsxwriter)
        include(ExternalProject)

            ### https://runebook.dev/ja/docs/cmake/module/externalproject
            ExternalProject_Add(
                xlsxwriter
                GIT_REPOSITORY https://github.com/jmcnamara/libxlsxwriter.git
                GIT_TAG main
                PREFIX     ${EXTERNAL_LIBBUILD_DIR}
                CMAKE_GENERATOR "Ninja"
                CMAKE_ARGS
                    -DZLIB_LIBRARY=${EXTERNAL_LIBRARY_PATH}/lib
                    -DZLIB_INCLUDE_DIR=${EXTERNAL_LIBRARY_PATH}/include
                    -DCMAKE_INSTALL_PREFIX=${EXTERNAL_LIBRARY_PATH}
                    -DCMAKE_BUILD_TYPE=Release
            )

        add_dependencies(xlsxwriter zlibstatic)
        add_dependencies(${REAL_LIBNAME} xlsxwriter)

    endif()

set(DEPENDS_LIBRARIES xlsxwriter)

## load Python CAPI Extentions Package
### https://scikit-build.readthedocs.io/en/latest/cmake-modules/PythonExtensions.html#example-usage
find_package(Python3 COMPONENTS Interpreter Development)
    set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${Python3_SITELIB}/skbuild/resources/cmake)
    find_package(PythonExtensions REQUIRED)

    add_library(${REAL_LIBNAME} MODULE ${LIBRARY_SOURCES})
        target_include_directories(${REAL_LIBNAME} PRIVATE ${CMAKE_INSTALL_PREFIX}/include)
        target_link_directories(${REAL_LIBNAME} PRIVATE ${Python3_LIBRARY_DIRS} ${CMAKE_INSTALL_PREFIX}/lib)

        ### If Exists Depends Project ###
        target_link_libraries(${REAL_LIBNAME} ${DEPENDS_LIBRARIES})
    
    python_extension_module(${REAL_LIBNAME})

    install(
        TARGETS
            ${REAL_LIBNAME}
        LIBRARY DESTINATION ${CMAKE_PROJECT_NAME}
    )

    ## executable file install
    ### https://scikit-build.readthedocs.io/en/latest/cmake-modules/PythonExtensions.html#command:python_standalone_executable
    IF (DEFINED EXENAME AND EXISTS EXE_SOURCES)
        python_standalone_executable(${EXENAME})
    ENDIF()


# Install to ${CMAKE_INSTALL_PREFIX} directory
install(TARGETS ${CMAKE_PROJECT_NAME}
    RUNTIME        DESTINATION . # bin
    LIBRARY        DESTINATION . # lib
    ARCHIVE        DESTINATION . # lib
    PRIVATE_HEADER DESTINATION . # include
    PUBLIC_HEADER  DESTINATION . # include
)
