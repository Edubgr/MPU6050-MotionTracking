from plot2d import *
from plot3d import *
import matplotlib.animation as animation
from matplotlib import pyplot as plt

print('acc = Aceleração do corpo')
print('vel = Velocidade do corpo integrando a aceleração sem correção')
print('pos = Posição do corpo integrando a velocidade sem correção')
print('veld = Velocidade do corpo integrando a aceleração retirando o drift')
print('posd = Posição do corpo integrando a velocidade com correção')
print('quat = Quaternion obtido pelo sensor')
print('quatc = Quaternion real do corpo')
print('euler = Rotação em graus do corpo')


print('Siga as perguntas para plotar o gráfico desejado')
print('Escreva "help" caso tenha duvida do significado')
print('Para voltar escreva "back"')

while(True):
    reset=0
    type_display=input('Save(0) or Show(1): ')
    if type_display == 'help':
        print('Você que salvar o gráfico ou apenas mostrá-lo?')
    elif type_display == '0' or type_display == '1':
        while(reset==0):
            AorS=input('Animate(0) or Static(1): ')
            if AorS == 'help':
                print('Você quer um gráfico com animação ou parado?')
            elif AorS == '0' or AorS == '1':
                while(reset==0):
                    dimension=input('2d(0) or 3d(1): ')
                    if dimension == 'help':
                        print('Você quer um gráfico 2d ou 3d?')
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
                                        print('Você quer usar um arquivo ou mais de um?')
                                    elif plot == '0':
                                        while(reset==0):
                                            plot=input('One col(0) or Three plot(1): ')
                                            if plot == 'help':
                                                print('Você que apenas linhas ou um grafico com 3 plots?')
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
                                        print('Você quer qual tipo de plot:')
                                    elif plot == '0' or plot == '1' or plot == '2':
                                        ani=plot3d_animate(plot)
                                        reset=1
                                    elif plot == 'back':
                                        break
                            elif AorS == '1':
                                while(reset==0):
                                    plot=input('Position(0) or Position and Rotation(1): ')
                                    if plot == 'help':
                                        print('Você quer qual tipo de plot:')
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
                ani.save('plot'+'_'+dimension+'_'+plot+'.mp4', writer=animation.FFMpegWriter(fps=60))
            elif AorS == '1':
                plt.savefig('plot'+'_'+dimension+'_'+plot+'.png')
            print('Save archive of type: '+AorS+' dimension: '+dimension+' and plot type: '+plot)
            print("Done")
            plt.close()
        elif type_display == '1':
            plt.show()
            print('Show archive of type: '+AorS+' dimension: '+dimension+' and plot type: '+plot)