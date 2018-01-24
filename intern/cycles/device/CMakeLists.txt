
#add_subdirectory(bcd/ext/eigen)
set(INC
	..
	../../glew-mx

)

set(INC_SYS
	${GLEW_INCLUDE_DIR}
	../../../extern/clew/include
	../../../extern/Eigen3 # for eigen in denoisingunit.h
)

set(INC_BCD
	bcd/BayesianCollaborativeDenoiser
	bcd/Common
	bcd/Common/exr
)

if(WITH_CUDA_DYNLOAD)
	list(APPEND INC
		../../../extern/cuew/include
	)
	add_definitions(-DWITH_CUDA_DYNLOAD)
else()
	list(APPEND INC_SYS
		${CUDA_TOOLKIT_INCLUDE}
	)
	add_definitions(-DCYCLES_CUDA_NVCC_EXECUTABLE="${CUDA_NVCC_EXECUTABLE}")
endif()

set(SRC
	device.cpp
	device_cpu.cpp
	device_cuda.cpp
	device_denoising.cpp
	device_memory.cpp
	device_multi.cpp
	device_opencl.cpp
	device_split_kernel.cpp
	device_task.cpp
)

set(SRC_OPENCL
	opencl/opencl.h
	opencl/memory_manager.h

	opencl/opencl_base.cpp
	opencl/opencl_mega.cpp
	opencl/opencl_split.cpp
	opencl/opencl_util.cpp
	opencl/memory_manager.cpp
)


SET(bcd_folder "${CMAKE_CURRENT_SOURCE_DIR}/bcd")
SET(bayesian_folder "${bcd_folder}/BayesianCollaborativeDenoiser")
SET(common_folder "${bcd_folder}/Common")
SET(exr_folder "${common_folder}/exr")
SET(bcd_cli "${bcd_folder}/bcd_cli")

SET(SRC_BCD
	${bayesian_folder}/Denoiser.cpp
	${bayesian_folder}/DenoisingUnit.cpp
	${bayesian_folder}/MultiscaleDenoiser.cpp
	${bayesian_folder}/SpikeRemovalFilter.cpp
	${bayesian_folder}/SamplesAccumulator.cpp
	${common_folder}/Chronometer.cpp
	${common_folder}/ImageIO.cpp
	${common_folder}/Utils.cpp
	${common_folder}/DeepImage.hpp
	${common_folder}/CovarianceMatrix.cpp
	${exr_folder}/io_exr.cpp
	${bayesian_folder}/CudaHistogramDistance.cu
)

SET(SRC_BCD_HEADERS
	${bayesian_folder}/IDenoiser.h
	${bayesian_folder}/Denoiser.h
	${bayesian_folder}/DenoisingUnit.h
	${bayesian_folder}/MultiscaleDenoiser.h
	${bayesian_folder}/SpikeRemovalFilter.h
	${bayesian_folder}/SamplesAccumulator.h
	#${bayesian_folder}/Launch.h
	${common_folder}/DeepImage.h
	${common_folder}/Chronometer.h
	${common_folder}/ImageIO.h
	${common_folder}/Utils.h
	${common_folder}/CovarianceMatrix.h
	${exr_folder}/io_exr.h
	${bayesian_folder}/CudaHistogramDistance.h
)

if(WITH_CYCLES_NETWORK)
	list(APPEND SRC
		device_network.cpp
	)
endif()

set(SRC_HEADERS
	device.h
	device_denoising.h
	device_memory.h
	device_intern.h
	device_network.h
	device_split_kernel.h
	device_task.h
)

add_definitions(${GL_DEFINITIONS})
if(WITH_CYCLES_NETWORK)
	add_definitions(-DWITH_NETWORK)
endif()
if(WITH_CYCLES_DEVICE_OPENCL)
	add_definitions(-DWITH_OPENCL)
endif()
if(WITH_CYCLES_DEVICE_CUDA)
	add_definitions(-DWITH_CUDA)
endif()
if(WITH_CYCLES_DEVICE_MULTI)
	add_definitions(-DWITH_MULTI)
endif()

include_directories(${INC})
include_directories(SYSTEM ${INC_SYS})
include_directories(${INC_BCD})

#add_compile_options("-libiomp")
add_compile_options("-fopenmp")
#link_directories("/usr/local/Cellar/llvm/5.0.0/lib")
add_library(cycles_device ${SRC} ${SRC_OPENCL} ${SRC_HEADERS} ${SRC_BCD} ${SRC_BCD_HEADERS})
#target_link_libraries(cycles_device omp)
