from plot2d import *
from plot3d import *
import matplotlib.animation as animation
from matplotlib import pyplot as plt

print('acc = Body acceleration')
print('vel = Body speed integrating acceleration without correction')
print('pos = Body position integrating speed without correction')
print('veld = Body velocity integrating acceleration removing drift')
print('posd = Body position integrating velocity with correction')
print('quat = Quaternion obtained by the sensor')
print('quatc = Real body quaternion')
print('euler = Rotation in radians of the body without correction')
print('eulerc = Rotation in radians of the body with correction')
print('\n')


print('Follow the questions to plot the desired graph.')
print('Write "help" if you have any doubts about the meaning.')
print('To go back write "back"')
print('\n')


while(True):
    reset=0
    type_display=input('Save(0) or Show(1): ')
    if type_display == 'help':
        print('Do you want to save the graph or just show it?')
    elif type_display == '0' or type_display == '1':
        while(reset==0):
            AorS=input('Animate(0) or Static(1): ')
            if AorS == 'help':
                print('Do you want an animated or still graphic?')
            elif AorS == '0' or AorS == '1':
                while(reset==0):
                    dimension=input('2d(0) or 3d(1): ')
                    if dimension == 'help':
                        print('Do you want a 2d or 3d chart?')
                    elif dimension == '0':
                        while(reset==0):
                            if AorS == '0':
                                ani = plot2d_animated()
                                plot='0'
                                reset=1
                            elif AorS == '1':
                                while(reset==0):
                                    plot=input('One Data(0) or More one Data(1): ')
                                    if plot == 'help':
                                        print('Do you want to use one file or more than one?')
                                    elif plot == '0':
                                        while(reset==0):
                                            plot=input('One col(0) or Three plot(1): ')
                                            if plot == 'help':
                                                print('Do you want just lines or a graph with 3 plots?')
                                            elif plot == '0':
                                                fig=plot2d_static_onecol()
                                                reset=1
                                            elif plot == '1':
                                                fig=plot2d_static_threeplot()
                                                reset=1
                                            elif plot == 'back':
                                                break
                                    elif plot == '1':
                                        fig=plot2d_static_moredata()
                                        plot='2'
                                        reset=1
                                    elif plot == 'back':
                                        break
                    elif dimension == '1':
                        while(reset==0):
                            if AorS == '0':
                                while(reset==0):
                                    plot=input('Rotation(0), Position(1) or Position and Rotation(2): ')
                                    if plot == 'help':
                                        print('What kind of plot do you want?')
                                    elif plot == '0' or plot == '1' or plot == '2':
                                        ani=plot3d_animate(plot)
                                        reset=1
                                    elif plot == 'back':
                                        break
                            elif AorS == '1':
                                while(reset==0):
                                    plot=input('Position(0) or Position and Rotation(1): ')
                                    if plot == 'help':
                                        print('What kind of plot do you want?')
                                    elif plot == '0':
                                        fig=plot3d_static_pos()
                                        reset=1
                                    elif plot == '1':
                                        fig=plot3d_static_posrot()
                                        reset=1
                                    elif plot == 'back':
                                        break
                    elif dimension == 'back':
                        break
            elif AorS == 'back':
                break
    elif type_display == 'quit':
        quit()
    if reset == 1:
        if type_display == '0':
            if AorS == '0':
                ani.save('plot'+'_'+dimension+'_'+plot+'.mp4', writer=animation.FFMpegWriter(fps=100))
            elif AorS == '1':
                #fig.set_size_inches(15, 4)
                plt.savefig('plot'+'_'+dimension+'_'+plot+'.png',dpi=200)
            print('Save archive of type: '+AorS+' dimension: '+dimension+' and plot type: '+plot)
            print("Done")
            plt.close()
        elif type_display == '1':
            plt.show()
            print('Show archive of type: '+AorS+' dimension: '+dimension+' and plot type: '+plot)