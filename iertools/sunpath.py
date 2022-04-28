def sunpath():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import datetime
    from ipywidgets import widgets,interact
    def angulo(phi,day,hour):
        np.seterr(invalid='ignore')
        days  = np.arange(1, 365/2+1,21)
        rad = np.pi/180.; deg = 180./np.pi; contador =  0 
        r = [] 
        angulo = []
        etiqueta = []
        for d in days:
            delta = 23.5*np.sin( (360*(284+d)/365)*rad )
            ortho = deg*np.arccos (-1.*np.tan(rad*phi)*np.tan(rad*delta))
            r.append([])
            angulo.append([])
            fecha = datetime.datetime.strptime(str(int(d)), '%j').date()
            etiqueta.append(fecha.strftime('%d %B'))
            for h in np.arange(0,24 + .4 ,.4):
                omega = (h - 12.)*15.
                thetaz = np.arccos(np.cos(phi*rad)*np.cos(delta*rad)*np.cos(omega*rad) + np.sin(phi*rad)*np.sin(delta*rad))*deg
                gammas_d = np.arcsin(np.sin(omega*rad)*np.cos(delta*rad)/np.sin(thetaz*rad))*deg
                omega_ew = np.arccos(np.tan(delta*rad)/np.tan(phi*rad))*deg
                if (np.abs(omega)<omega_ew): C1 =  1.;
                else:  C1 = -1.;
                if (phi*(phi-delta) >= 0.): C2 =  1.;
                else: C2 = -1.;
                if (omega>=0.): C3 =  1.;
                else: C3 = -1.;
                if (np.abs(np.tan(delta*rad)/np.tan(phi*rad)) > 1. ): C1 =  1.;
                gamma_s = C1 * C2 *  gammas_d  + C3 *(1. - C1*C2 )*180./2.
                alpha_s = 90.-thetaz
                r[contador].append( np.sin((45.-alpha_s/2.)*rad)/np.sin((135.-alpha_s/2.)*rad)*90 )   
                if (phi >= 0.):  angulo[contador].append(1.*(gamma_s-90))
                else: angulo[contador].append(1.*(gamma_s-90.)+180)
            contador = contador + 1            
        angulo = np.array(angulo)
        r = np.array(r)
        #CALCULO PARA LA L'INEA DE 1 D'IA
        r_day = []
        angulo_day = []
        delta = 23.5*np.sin( (360*(284+day)/365)*rad )
        ortho = deg*np.arccos (-1.*np.tan(rad*phi)*np.tan(rad*delta))
        for h in np.arange(0,24 + .4 ,.4):
            omega = (h - 12.)*15.
            thetaz = np.arccos(np.cos(phi*rad)*np.cos(delta*rad)*np.cos(omega*rad) 
                               + np.sin(phi*rad)*np.sin(delta*rad))*deg
            gammas_d = np.arcsin(np.sin(omega*rad)*np.cos(delta*rad)/np.sin(thetaz*rad))*deg
            omega_ew = np.arccos(np.tan(delta*rad)/np.tan(phi*rad))*deg
            if (np.abs(omega)<omega_ew): C1 =  1.;
            else:  C1 = -1.;
            if (phi*(phi-delta) >= 0.): C2 =  1.;
            else: C2 = -1.;
            if (omega>=0.): C3 =  1.;
            else: C3 = -1.;
            if (np.abs(np.tan(delta*rad)/np.tan(phi*rad)) > 1. ): C1 =  1.;
            gamma_s = C1 * C2 *  gammas_d  + C3 *(1. - C1*C2 )*180./2.
            alpha_s = 90.-thetaz
            r_day.append( np.sin((45.-alpha_s/2.)*rad)/np.sin((135.-alpha_s/2.)*rad)*90 )   
            if (phi >= 0.):  angulo_day.append(1.*(gamma_s-90))
            else: angulo_day.append(1.*(gamma_s-90.)+180)          
        angulo_day = np.array(angulo_day) 
        r_day = np.array(r_day) 
        #CALCULO PARA  1 PUNTO
        r_hour = []
        angulo_hour = []
        ortho = deg*np.arccos (-1.*np.tan(rad*phi)*np.tan(rad*delta))
        B = (day-1)* 360/365 *rad
        E = 229.2*(0.000075 + 0.001868 * np.cos(B) - 0.032077*np.sin(B)
                   - 0.014615*np.cos(2*B) - 0.04089*np.sin(2*B))
        omega = (hour-E/60 - 12.)*15.
        thetaz = np.arccos(np.cos(phi*rad)*np.cos(delta*rad)*np.cos(omega*rad) 
                           + np.sin(phi*rad)*np.sin(delta*rad))*deg
        gammas_d = np.arcsin(np.sin(omega*rad)*np.cos(delta*rad)/np.sin(thetaz*rad))*deg
        omega_ew = np.arccos(np.tan(delta*rad)/np.tan(phi*rad))*deg
        if (np.abs(omega)<omega_ew): C1 =  1.;
        else:  C1 = -1.;
        if (phi*(phi-delta) >= 0.): C2 =  1.;
        else: C2 = -1.;
        if (omega>=0.): C3 =  1.;
        else: C3 = -1.;
        if (np.abs(np.tan(delta*rad)/np.tan(phi*rad)) > 1. ): C1 =  1.;
        gamma_s = C1 * C2 *  gammas_d  + C3 *(1. - C1*C2 )*180./2.
        alpha_s = 90.-thetaz
        r_hour.append( np.sin((45.-alpha_s/2.)*rad)/np.sin((135.-alpha_s/2.)*rad)*90 )   
        if (phi >= 0.):  angulo_hour.append(1.*(gamma_s-90))
        else: angulo_hour.append(1.*(gamma_s-90.)+180)          
        angulo_hour = np.array(angulo_hour) 
        r_hour = np.array(r_hour) 
    #COMIENZA EL CALCULO DE LAS ANALEMAS
        days_analema = np.arange(1,365,1)
        angulo_horario = []
        r_horario = []
        contador_r =  0 
        for h in np.arange(0,24+1,1):
            r_horario.append([])
            angulo_horario.append([])
            for d in days_analema:
                delta = 23.5*np.sin( (360*(284+d)/365)*rad )  
                B = (d-1)* 360/365 *rad
                E = 229.2*(0.000075 + 0.001868 * np.cos(B) - 0.032077*np.sin(B)
                 - 0.014615*np.cos(2*B) - 0.04089*np.sin(2*B))
                omega = (h -E/60 - 12.)*15.
                thetaz = np.arccos(np.cos(phi*rad)*np.cos(delta*rad)*np.cos(omega*rad) + np.sin(phi*rad)*np.sin(delta*rad))*deg
                gammas_d = np.arcsin(np.sin(omega*rad)*np.cos(delta*rad)/np.sin(thetaz*rad))*deg
                omega_ew = np.arccos(np.tan(delta*rad)/np.tan(phi*rad))*deg        
                if (np.abs(omega)<omega_ew): C1 =  1.;
                else:  C1 = -1.;
                if (phi*(phi-delta) >= 0.): C2 =  1.;
                else: C2 = -1.;
                if (omega>=0.): C3 =  1.;
                else: C3 = -1.;
                if (np.abs(np.tan(delta*rad)/np.tan(phi*rad)) > 1. ): C1 =  1.;    
                gamma_s = C1 * C2 *  gammas_d  + C3 *(1. - C1*C2 )*180./2.
                alpha_s = 90.-thetaz
                r_horario[contador_r].append( np.sin((45.-alpha_s/2.)*rad)/np.sin((135.-alpha_s/2.)*rad)*90 )
                if (phi >= 0.):  angulo_horario[contador_r].append(1.*(gamma_s-90))
                else: angulo_horario[contador_r].append(1.*(gamma_s-90.)+180)
            contador_r = contador_r + 1
        angulo_horario = np.array(angulo_horario) 
        r_horario = np.array(r_horario) 
        rad = np.pi/180.; deg = 180./np.pi; contador =  0
#         plt.xkcd()
        plt.figure(figsize=(10,10))
        ax = plt.subplot(111, projection='polar')
    #     print(ax.annotate.__doc__)
        for d in range(len(angulo)):
            ax.plot(angulo[d]*rad,r[d],color='gray',linewidth=2)
            ax.annotate(etiqueta[d],xy=(0,0),xytext=(d*rad*9-30*rad,92),xycoords='data') 
        for a in range(len(r_horario)):
            ax.plot(angulo_horario[a]*rad,r_horario[a],color='red',linewidth=1)
        ax.plot(angulo_day*rad,r_day,color='green',linewidth=3)
        ax.scatter(angulo_hour*rad,r_hour,color='red',s=250)
        ax.set_rlabel_position(90) 
        ax.set_rticks(range(0,90,10))
        ax.grid(color = 'gray', linestyle = 'dotted', linewidth = 1 )
        ax.set_rmax(90)
        ax.set_rmin(0)        
        ax.grid()

    #     plt.title('Stereographic sun path diagram',)
        plt.show()
#         plt.savefig('stereograph.png')
#     print(etiqueta)
    
    interact(angulo,phi = (.5,89.,.5),day=(1,365,10),hour=(0,24,1))
#     angulo(18.5,1,0)
    return 