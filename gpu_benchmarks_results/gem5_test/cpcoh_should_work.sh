#!/bin/bash

# Inputs: benchmark path, benchmark bin, num_sched_gpu, baseline_or_cpcoh, benchmark options,
# Arg5 = "baseline" if running chunk scheduler with baseline

echo "Arg1: "$1"";
export benchmark_root="$1"
shift
echo "Arg2: "$1"";
export output_dir="$1"
#echo $output_dir
shift
echo "Arg3: "$1"";
export benchmark_name="$1"
shift
echo "Arg4: "$1"";
export l2size="$1"
shift
echo "Arg5: "$1"";
export replace_policy="$1"
shift
echo "Arg6: "$*"";
export benchmark_options="$*"
export LD_LIBRARY_PATH=/usr/lib
mkdir -p m5out.$output_dir
# make -C multigpu_benchmarks/rodinia_host/backprop/

# if [ "$2" = "rnn_bench_sync" ]; then
#     cp -a multigpu_benchmarks/cachefiles/. /.cache/miopen/1.7.0/
# fi


build/VEGA_X86/gem5.opt -r -d m5out.$output_dir configs/example/apu_se.py \
    -n 3 --dgpu --gfx-version=gfx900 --num-compute-units=60 \
   --cu-per-sa=15 --num-gpu-complex=4 --reg-alloc-policy=dynamic --num-tccs=8 \
    --num-dirs=64 --mem-size=16GB --mem-type=HBM_2000_4H_1x64 --vreg-file-size=16384 \
    --sreg-file-size=800 --tcc-size=$l2size --gpu-clock=1801MHz --ruby-clock=1000MHz --vrf_lm_bus_latency=6 \
    --mem-req-latency=69 --mem-resp-latency=69 --mandatory_queue_latency=1 --max-cu-tokens=160 \
    --max-coalesces-per-cycle=10 --sqc-size=16kB --scalar-mem-req-latency=28 --TCP_latency=4 --tcp-assoc=16 \
    --tcp-num-banks=16 --TCC_latency=121 --tcc-assoc=16 --tagAccessLatency=1 --dataAccessLatency=1 \
    --tcp-rp=LRURP --tcc-rp=$replace_policy \
    -c bin/$benchmark_name "--options=\"$benchmark_options\""