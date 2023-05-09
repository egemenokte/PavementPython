# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 16:36:51 2023

@author: egeme
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import python.iri as Rough
from scipy.signal import butter,filtfilt
import pandas as pd
from scipy.fft import fft, ifft
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse, Circle, Rectangle
import pandas as pd
#%%
road_profile=Rough.readxlsx('Profiles/Profile_0.xlsx',stick=0.25)
#%%
road_profile=Rough.readxlsx('Profiles/Profile_1.xlsx',stick=0.25)
#%%
road_profile=Rough.readxlsx('Profiles/Profile_2.xlsx',stick=0.25)
#%%
IRI, equidistant,ZZ = Rough.iri(road_profile, segment_length=20, start_pos=-1, step=0, box_filter = True, method = 2)
plt.close('all')
Rough.plot_iri(IRI,road_profile, 'Roughness')
Rough.plot_mass(ZZ, 'Displacements')
#%%
plt.close('all')
# sns.set()
save=False
resx=20 #in meters
usdist=0.15/2 #distance from road
sdist=0.2 #distance from road
distbet=sdist-usdist
US=ZZ[:,1]+usdist
S=ZZ[:,0]+sdist
US=US
S=S
X=ZZ[:,2]
R=ZZ[:,3]
dif=X[1]-X[0]
IRIi=ZZ[:,4]
IRIc=np.cumsum(IRIi)/(np.arange(len(IRIi))+1)
fig, ax = plt.subplots(figsize=(7,5))
if save:
    im = plt.imread('python/dd2.png')
    newax = fig.add_axes([0.77,0.74,0.12,0.12], anchor='NE', zorder=1)
    newax.imshow(im)
    newax.axis('off')
def animate(i):

    ax.clear()
    Xp=X[max(0,i-int(resx/dif)):i+int(resx/dif)+1]
    Rp=R[max(0,i-int(resx/dif)):i+int(resx/dif)+1]
    ax.fill(np.append(Xp,[max(Xp),min(Xp)]), np.append(Rp,[min(Rp)-0.1,min(Rp)-0.1]),color='dimgray') #draw the road
    x,y=Rough.spring((X[i], R[i]),(X[i], US[i]),8,resx/20) #draw the first spring from road to unsprung
    ax.plot(x,y,color='grey',zorder=1)
    x,y=Rough.spring((X[i]-resx/10*3/5, US[i]),(X[i]-resx/10*3/5, S[i]),10,resx/20) #seond spring between masses
    ax.plot(x,y,color='grey',zorder=1)
    
    ax.plot([X[i]+resx/10*3/5, X[i]+resx/10*3/5],[US[i],US[i]+distbet/2],color='grey',zorder=1)
    ax.plot([X[i]+resx/10*3/5-resx/40, X[i]+resx/10*3/5+resx/40],[US[i]+distbet/2,US[i]+distbet/2],color='grey',zorder=1)
    ax.plot([X[i]+resx/10*3/5, X[i]+resx/10*3/5],[S[i],S[i]-distbet/2*0.6],color='grey',zorder=1)
    ax.plot([X[i]+resx/10*3/5-resx/30, X[i]+resx/10*3/5+resx/30],[S[i]-distbet/2*0.6,S[i]-distbet/2*0.6],color='grey',zorder=1)
    ax.plot([X[i]+resx/10*3/5-resx/30, X[i]+resx/10*3/5-resx/30],[S[i]-distbet/2*0.6,S[i]-distbet/2*1.2],color='grey',zorder=1)
    ax.plot([X[i]+resx/10*3/5+resx/30, X[i]+resx/10*3/5+resx/30],[S[i]-distbet/2*0.6,S[i]-distbet/2*1.2],color='grey',zorder=1)
    
    ax.scatter(X[i], R[i],color='black',zorder=2) # draw a ball on the road profile
    ax.plot(X[i-int(resx/dif):i+1], US[i-int(resx/dif):i+1],zorder=1,color='midnightblue') #unsprung mass history
    ax.plot(X[i-int(resx/dif):i+1], S[i-int(resx/dif):i+1],zorder=1,color='darkred') #sprung mass history
    
    ax.add_patch(Rectangle((X[i]-resx/10, US[i]-sdist/20), resx/5, sdist/10,color='midnightblue')) #unsprung mass
    ax.add_patch(Rectangle((X[i]-resx/10, S[i]-sdist/20), resx/5, sdist/10,color='darkred')) #sprung mass
    
    ax.text(X[max(0,i-int(resx/dif))]+sdist/2, R[i]-sdist/2.1, f"IRI Instant. = {np.round(IRIi[i],1)} m/km", size=15, color='Black')
    ax.text(X[max(0,i-int(resx/dif))]+sdist/2, R[i]+sdist*1.5, f"IRI Overall = {np.round(IRIc[i],1)} m/km", size=15, color='Black')


    ax.set_xlim([X[max(0,i-int(resx/dif))],X[i+int(resx/dif)]])
    ax.set_ylim([R[i]-sdist/2,R[i]+sdist*3/2])
    ax.grid(False)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticks([X[max(0,i-int(resx/dif))],X[i+int(resx/dif)]],['',str(2*resx)+'m'])
    # implot = plt.imshow(im,aspect='auto',zorder=0,extent=[X[max(0,i-int(resx/dif))],X[i+int(resx/dif)], R[i]-0.1, R[i]+0.3])

ani = FuncAnimation(fig, animate, frames=1000, interval=0.1*dif, repeat=True,repeat_delay = 300)
plt.show()
if save:
    ani.save('tr3.gif',fps=30, dpi=100)

