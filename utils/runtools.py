from multiprocessing import Pool,cpu_count,current_process 
import subprocess
from .logtools import print_info, print_error, print_warn



def RunCMD(cmd):
    print_info('run command : %s' % cmd)
    
    def swap_log(swap, error = True):
        sinfo = []
        for l in swap.split('\n'):
            if l == '':
                continue
            sinfo.append(l)
        for o in sinfo:
            if error:
                print_error(o) 
            else:
                print_info(o) 
        return            
    output = subprocess.run(cmd, 
                            shell=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)    
    status = output.returncode
    stdout = output.stdout
    stderr = output.stderr
    
    if status != 0:
        if output.stdout:
             swap_log(output.stdout, error=True)
        if output.stderr:
             swap_log(output.stderr, error=True)
    else:
        if output.stdout:
            swap_log(output.stdout, error=False)
    #return status

    return status, stdout, stderr



def MultiProcessRun(func, deal_list, n_cpus=None):

    #round_c = [deal_list[i:i+batch_size] for i  in range(0, len(deal_list), batch_size)]
    #mata thinking: https://my.oschina.net/leejun2005/blog/203148
    if n_cpus ==None:
        N_CPUS = cpu_count()
    else:
        N_CPUS = int(n_cpus)

    print_info('the number of process is %s' % N_CPUS)

    pool = Pool(N_CPUS)
    a = pool.map(func, deal_list)
    pool.close()
    pool.join()
    return a