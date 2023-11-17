#%%
from Libraries import *
from Datastructures import Custom_body_1 as custom
from MAIN import *
# %%
with open('1700148827.3789582_random_search.pkl', 'rb') as file:
        data = pickle.load(file)
# %%
x = np.array([i for i in range(len(data[1]))])
y = np.zeros(len(data[1]))
for i,fit in enumerate(data[1]):
    if i == 0:
        y[i] = fit
    else:
        if fit >= y[i-1]:
            y[i] = fit
        else:
            y[i] = y[i-1]
print(x)
print(y)
# %%
# PLOT LEARNING CURVE
plt.figure(figsize=(10, 10))
plt.plot(x, y, '-', label='RS', color='#3CB371')
plt.title("Random Search Learning Curve")
plt.xlabel('Evaluations')
plt.ylabel('fitness (distance in [m] after 20s)')
plt.legend()
plt.grid(True)
plt.savefig('RS_Learning_Curve_{}evals.pdf'.format(len(data[1])), dpi=300)
plt.show()
# %%
