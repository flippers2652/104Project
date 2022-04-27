import pyreadr
import matplotlib.pyplot as plt
from numpy import mean,std
from scipy.stats import sem,norm,probplot,skew
import subprocess
import math
def sigfig(x,s):
    return round(x, s - int(math.floor(math.log10(abs(x)))) - 1)



# Read the data
result = pyreadr.read_r('./PROJ.Rdata') # also works for Rds
ID=143
data=result['PROJ'].values[ID-1]

# 1. Calculate the sample mean.
xbar=mean(data)
# 2. Calculate the sample standard deviation. 
sd=std(data,ddof=1)

# 4. Discuss if assumptions required for the sample mean to be nearly normal are satisfied (3 sentences max).
# Histogram
plt.hist(data,bins=range(-50,61,10),color="m")
plt.plot(range(-50,55),400*norm.pdf(range(-50,55),xbar,sd),color="c")
plt.title("Histogram")
plt.xlabel("Stock Price Returns")
plt.ylabel("Quantity")
plt.savefig("hist.png",dpi=500)

# QQ
plt.figure("qq")
print(norm.cdf(data,xbar,sd))
plt.scatter(norm.ppf([(2*i+1)/80 for i in range(0,40)],xbar,sd),sorted(data),marker="o",color="g",zorder=20)
plt.plot(range(-50,35),range(-50,35),color="r")

#probplot(data, dist=norm(xbar,sd), plot=plt)
plt.title("QQ Plot")
plt.xlabel("Expected Stock Price Returns")
plt.ylabel("Sample Stock Price Returns")
plt.savefig("qq.png",dpi=500)

sk=skew(data)

#5. Assuming the assumptions are satisfied, calculate the standard error of the mean.
se=sem(data)

# 6. Calculate a 95% confidence interval for the average year-to-date stock return of S&P 500 companies.
interval95=norm.interval(0.95, loc=mean(data), scale=sem(data))

# 7. Calculate a 99% confidence interval for the average year-to-date stock return of S&P 500 companies.
interval99=norm.interval(0.99, loc=mean(data), scale=sem(data))

# 8. Perform a hypothesis test which tests if the average year-to-date stock return of S\&P 500 companies is equal to zero. Clearly setup your hypothesis test and report a p-value (to 3 significant figures).
pvalue=norm.sf(0,mean(data),sem(data))*2


# Output to python.sty to give the values to latex
with open("python.sty","w") as file:
    def writedef(file,key,value):
        file.write("\\newcommand{\\"+key+"}"+"{"+value+"}"+"\n")
        
    file.write("\ProvidesPackage{python}\n")
    writedef(file,"data","\\begin{tabularx}{0.8\\textwidth}{ "+">{\\raggedleft\\arraybackslash}X"*5+" }"+(", ").join("&"*(x%5!=0)+"\\\\\n"*(x%5==0 and x!=0)+(x==0)*"\n"+format(data[x], "6.3f") for x in range(len(data)))+"\\end{tabularx}")
    writedef(file,"xbar",format(xbar, ".3f"))
    writedef(file,"sd",format(sd, ".3f"))
    writedef(file,"se",format(se, ".3f"))
    writedef(file,"intervalA","("+format(interval95[0], ".3f")+", "+format(interval95[1], ".3f")+")")
    writedef(file,"intervalB","("+format(interval99[0], ".3f")+", "+format(interval99[1], ".3f")+")")
    writedef(file,"pvalue","{:.{}f}".format( pvalue, 3 - int(math.floor(math.log10(abs(pvalue)))) - 1 ))
    writedef(file,"sk","{:.{}f}".format( sk, 3 - int(math.floor(math.log10(abs(pvalue)))) - 1 ))

#Compile to pdf
subprocess.run(["pdflatex","main.tex"])

