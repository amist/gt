# For log 0 - weight_100.log
w_wsahara = [57 ,45 ,54 ,57 ,57 ,39 ,93 ,47 ,52 ,40 ,44 ,50 ,41 ,54 ,56 ,74 ,72 ,54 ,55 ,60 ,47 ,47 ,61 ,51 ,53 ,60 ,58 ,55 ,93 ,60 ,49 ,49 ,50 ,52 ,44 ,51 ,52 ,49 ,64 ,53 ,103,71 ,39 , ]
# --> Succeeded 43 out of 100 tries with an average of 56.09 generations
# For log 1 - diff_100.log
d_wsahara = [31,57,47,35,54,59,62,43,38,57,42,50,50,41,45,48,60,68,51,61,37,87,53,71,61,43,60,36,53,56,37,51,45,54,50,43,41,57,52,43,47,48,49,54, ]
# --> Succeeded 44 out of 99 tries with an average of 50.61 generations

import scipy.stats

print(scipy.stats.ttest_ind(w_wsahara, d_wsahara))
