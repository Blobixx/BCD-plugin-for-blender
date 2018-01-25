# This file is part of the reference implementation for the paper 
#   Bayesian Collaborative Denoising for Monte-Carlo Rendering
#   Malik Boughida and Tamy Boubekeur.
#   Computer Graphics Forum (Proc. EGSR 2017), vol. 36, no. 4, p. 137-153, 2017
#
# All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE.txt file.

CMAKE_MINIMUM_REQUIRED(VERSION 2.8.8)

#PROJECT(BayesianCollaborativeDenoising)

OPTION(BCD_BUILD_GUI "Build a GUI executable for bcd, using library NanoGUI" OFF)
OPTION(BCD_USE_CUDA "Use CUDA for accelerating computations" ON)

# Add CMake folder to the  module path : contains CMake specific files *.cmake
SET(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMake" ${CMAKE_MODULE_PATH} )

# Set the default build to Release.  Note this doesn't do anything for the VS
# default build target which defaults to Debug when you first start it.
IF(NOT CMAKE_BUILD_TYPE)
	SET(CMAKE_BUILD_TYPE "Debug" CACHE STRING
		"Choose the type of build, options are: Debug Release RelWithDebInfo MinSizeRel."
		FORCE)
ENDIF(NOT CMAKE_BUILD_TYPE)







# OpenMP
FIND_PACKAGE(OpenMP)

IF(${CMAKE_VERSION} VERSION_GREATER 3.8)

	# not tested yet
	MESSAGE(AUTHOR_WARNING "Using OpenMP detection from cmake 3.9.0+: not tested yet")
	IF(OPENMP_CXX_FOUND)
		ADD_LIBRARY(OpenMP ALIAS OpenMP::OpenMP_CXX)
	ELSE()
		MESSAGE(WARNING "Could not find OpenMP library")
	ENDIF()

ELSE()

	IF(OPENMP_FOUND)
		ADD_LIBRARY(OpenMP INTERFACE)
		TARGET_COMPILE_OPTIONS(OpenMP INTERFACE ${OpenMP_CXX_FLAGS})
		TARGET_LINK_LIBRARIES(OpenMP INTERFACE
				$<$<CXX_COMPILER_ID:GNU>:${OpenMP_CXX_FLAGS}>
				$<$<CXX_COMPILER_ID:Clang>:${OpenMP_CXX_FLAGS}>
				$<$<CXX_COMPILER_ID:Intel>:${OpenMP_CXX_FLAGS}>
				)
	ELSE()
		MESSAGE(WARNING "Could not find OpenMP library")
	ENDIF()

ENDIF()







IF(BCD_USE_CUDA)

	SET(CUDA_PROPAGATE_HOST_FLAGS OFF)
	FIND_PACKAGE(CUDA)

	IF(NOT CUDA_FOUND)
		MESSAGE(WARNING "Could not find CUDA")
	ELSE(NOT CUDA_FOUND)

		SET(CUDA_LIBRARIES PUBLIC ${CUDA_LIBRARIES}) # hack to avoid cmake warnings related to policy CMP0023 (see https://gitlab.kitware.com/cmake/cmake/issues/16602 )

		SET(config_types DEBUG RELEASE MINSIZEREL RELWITHDEBINFO)

		# We have to manually propagate all host flags but C++11...
		FOREACH(config ${config_types})
			SET(CUDA_NVCC_FLAGS_${config} "${CUDA_NVCC_FLAGS_${config}} -Xcompiler ")
	#		SET(CUDA_NVCC_FLAGS_${config} "${CUDA_NVCC_FLAGS_${config}} -g -lineinfo -Xcompiler ") #use this line instead of the previous one for debugging and line info (for nvprof for example)
			IF(OPENMP_FOUND)
				SET(CUDA_NVCC_FLAGS_${config} "${CUDA_NVCC_FLAGS_${config}},\"${OpenMP_CXX_FLAGS}\"")
			ENDIF(OPENMP_FOUND)
			STRING(REPLACE " " ";" FLAGS_LIST ${CMAKE_CXX_FLAGS_${config}})
			FOREACH(flag ${FLAGS_LIST})
				SET(CUDA_NVCC_FLAGS_${config} "${CUDA_NVCC_FLAGS_${config}},\"${flag}\"")
			ENDFOREACH()
		ENDFOREACH()
	ENDIF(NOT CUDA_FOUND)

	# Verbose option: put ON to see the whole build command lines
	IF(CUDA_FOUND)
		SET(CUDA_VERBOSE_BUILD ON)
	ENDIF(CUDA_FOUND)

ENDIF(BCD_USE_CUDA)






# Verbose option: put ON to see the whole build command lines
#SET(CMAKE_VERBOSE_MAKEFILE ON)

SET(bcd_folder_name "BayesianCollaborativeDenoiser")
SET(bcd_src_dir "${CMAKE_SOURCE_DIR}/intern/cycles/bcd")
SET(bcd_folder "${bcd_src_dir}/${bcd_folder_name}")
SET(common_folder "Common")
SET(exr_folder "${common_folder}/exr")


SET(bcd_library "")

#MESSAGE(STATUS "Entering subdirectory 'ext'")
#ADD_SUBDIRECTORY(ext)

#MESSAGE(STATUS "Entering subdirectory '${bcd_folder_name}'")
#ADD_SUBDIRECTORY(${bcd_folder_name})

#MESSAGE(STATUS "Entering subdirectory 'bcd_cli'")
# ADD_SUBDIRECTORY(bcd_cli)

#MESSAGE(STATUS "Entering subdirectory 'Raw2BcdInputs'")
# ADD_SUBDIRECTORY(Raw2BcdInputs)

IF(BCD_BUILD_GUI)
	ADD_SUBDIRECTORY(bcd_gui)
ELSE(BCD_BUILD_GUI)
	MESSAGE(STATUS "skipping building of GUI executable")
ENDIF(BCD_BUILD_GUI)

#INCLUDE(CPack)
set(INC
	..
	../../../extern/Eigen3
)

SET(src_files
	${bcd_folder_name}/Denoiser.cpp
	${bcd_folder_name}/DenoisingUnit.cpp
	${bcd_folder_name}/MultiscaleDenoiser.cpp
	${bcd_folder_name}/SpikeRemovalFilter.cpp
	${bcd_folder_name}/SamplesAccumulator.cpp
	${common_folder}/Chronometer.cpp
	${common_folder}/ImageIO.cpp
	${common_folder}/Utils.cpp
	${common_folder}/CovarianceMatrix.cpp
	${exr_folder}/io_exr.cpp
)
SET(header_files
	${bcd_folder_name}/IDenoiser.h
	${bcd_folder_name}/Denoiser.h
	${bcd_folder_name}/DenoisingUnit.h
	${bcd_folder_name}/MultiscaleDenoiser.h
	${bcd_folder_name}/SpikeRemovalFilter.h
	${bcd_folder_name}/SamplesAccumulator.h
	${bcd_folder_name}/Launch.h
	${common_folder}/DeepImage.h
	${common_folder}/Chronometer.h
	${common_folder}/ImageIO.h
	${common_folder}/Utils.h
	${common_folder}/CovarianceMatrix.h
	${exr_folder}/io_exr.h
)
SET(header_implementation_files
	${common_folder}/DeepImage.hpp
)

include_directories(${INC})
add_compile_options("-fopenmp")
add_library(bcd_library ${src_files} ${header_files} ${header_implementation_files})
