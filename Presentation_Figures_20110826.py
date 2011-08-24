import h5py
import criticality
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

figure_directory = '/home/jja34/public_html/Figures/' 
data_directory = '/work/imaging8/jja34/ECoG_Study/ECoG_Data/'
filter = 'filter_FIR_513_blackmanharris'

monkeys = (('A', 'food_tracking'), ('K1', 'food_tracking'), ('K2', 'visual_grating'), ('K2', 'rest'), ('K2', 'anesthesia'))
bands = ('beta', 'alpha', 'theta', 'delta')
recordings = range(5)
methods = (('events', 1), ('displacements', 2), ('amplitudes', 3), ('amplitude_aucs', 4))
for monkey, task in monkeys:
    for band in bands:
        if monkey == 'A':
            b = 3
            recordings = range(5)
        if monkey=='K1':
            recordings = range(3)
            b = 1
        if monkey=='K2':
            b = 1
            recordings = ''
            if task!='visual_grating':
                filter = 'filter_version0'
        for i in recordings:
            f = h5py.File(data_directory+'Monkey_'+monkey+'.hdf5')
            data = f[task+str(i)+'/'+filter+'/'+band]
            d = criticality.avalanche_analysis(data, bin_width=b)
        
            for method, fig in methods:
                X = d['size_'+method]
                plt.figure(fig)
                statistics.hist_log(X, X.max(), X.min())
                plt.xlabel('Size ('+method+')', fontsize='xx-large')
                plt.ylabel('P(Size)', fontsize='xx-large')
                plt.savefig(figure_directory+task+band+'_'+method+'_'+monkey)
                plt.title('Sizes as '+method+', '+band+' band,  Monkey '+monkey, fontsize='xx-large')
        plt.close('all')
