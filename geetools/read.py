
import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt
import ipython_genutils

class sql:
    def __init__(self,file,read="all",rename=False):
        
        self.myconn = sql.connect(file)
        if (read=="data") or (read=="all"):
            command = "SELECT ReportDataDictionaryIndex, KeyValue, Name, Units FROM ReportDataDictionary"
            variables = pd.read_sql_query(command,con=self.myconn)

            variables['variable_name'] = variables.KeyValue + ':' + variables.Name + ' (' + variables.Units + ')'
            self.variables = variables
            
            self.vars = variables.variable_name.unique()
            self.vars_numbered = [i for i in enumerate(self.vars)]
            

            command = "SELECT tm.TimeIndex, tm.Year, tm.Month, tm.Day, tm.Hour, tm.Minute FROM Time AS tm"
            time = pd.read_sql_query(command,con=self.myconn)
            time = time[time.Year!=0]
            command = """SELECT ReportData.TimeIndex, ReportData.ReportDataDictionaryIndex, ReportData.Value
              FROM (ReportData INNER JOIN ReportDataDictionary ON ReportData.ReportDataDictionaryIndex = ReportDataDictionary.ReportDataDictionaryIndex) 
              INNER JOIN Time ON ReportData.TimeIndex = Time.TimeIndex"""
            data = pd.read_sql_query(command,con=self.myconn)
            data_variables = pd.merge(data,self.variables)
            data_variables_time = pd.merge(data_variables,time)
            df = data_variables_time.copy()
            df['date'] = pd.to_datetime(df[['Year','Month','Day']])
            df.loc[df.Hour==24,'date'] += pd.Timedelta('1D')
            df.loc[df.Hour==24,'Hour'] = 0
            df['date'] = pd.to_datetime(df[['Year','Month','Day','Hour','Minute']])
            df['variable_name'] = df.KeyValue + ':' + df.Name + ' (' + df.Units + ')'
            df  = df.pivot_table(index="date", columns="variable_name", values="Value")
            self.data = df
        
            if rename:
                variables  = self.data.columns
                Ti_variables = ["Ti_"+variable.split(":")[0].replace(" ","") if "Zone Mean Air Temperature" in variable else variable for variable in variables]
                self.rename_cols(range(len(Ti_variables)),Ti_variables)
            
            
                variables  = self.data.columns
                Ti_variables = ["To" if "Site Outdoor Air Dry" in variable else variable for variable in variables]
                self.rename_cols(range(len(Ti_variables)),Ti_variables)
    
        
        if (read=="construction") or (read=="all"):
#             print("aca")
            command = """SELECT * FROM  Materials """
            m       = pd.read_sql_query(command,con=self.myconn)
            m = m.rename(columns={'Name': 'NameMaterial'})
            # 
            command = """SELECT * FROM  Constructions """
            c = pd.read_sql_query(command,con=self.myconn)
            c = c.rename(columns={'Name': 'NameConstruction'})
            # 
            command = """SELECT * FROM  ConstructionLayers """
            l = pd.read_sql_query(command,con=self.myconn)
            ml   = pd.merge(m,l)
            mlc = pd.merge(ml,c)
            self.mlc = mlc
            self.construction_systems = mlc.NameConstruction.unique()
            
    def rename_cols(self,columns,new_names):
        old_names = self.data.columns[columns]
        self.data.rename(columns=dict(zip(old_names, new_names)), inplace=True)
        self.vars = self.data.columns
        self.vars_numbered = [i for i in enumerate(self.vars)]
        
    def get_data(self,names):
        result = [variable for name in names for variable in self.vars if name in variable]
        return self.data[result]
    def get_construction(self,names_cs,round=4):
#         all = []
        for name_cs in names_cs:
            properties = ['NameMaterial','Conductivity', 'Density','SpecHeat', 'Thickness', 
                          'TotalLayers', 'InsideAbsorpVis', 'OutsideAbsorpVis','InsideAbsorpSolar',
                          'OutsideAbsorpSolar', 'InsideAbsorpThermal',
                          'OutsideAbsorpThermal', 'OutsideRoughness']
            cs = self.mlc.loc[self.mlc.NameConstruction==name_cs].sort_values('ConstructionLayersIndex')[properties]
            thickness =  cs['Thickness'].sum().round(round)
            total_layers = cs.TotalLayers.unique()
            InsideAbsopVis = cs.InsideAbsorpVis.unique()
            OutsideAbsopVis = cs.OutsideAbsorpVis.unique()
            OutsideAbsorpSolar = cs.OutsideAbsorpSolar.unique()
            InsideAbsorpThermal = cs.InsideAbsorpThermal.unique()
            OutsideAbsorpThermal = cs.OutsideAbsorpThermal.unique()
            OutsideRoughness = cs.OutsideRoughness.unique()
#             dictio = {'Construction system':name_cs,
#                       'Total thickness':thickness,
#                       'Total layers':total_layers,
#                       'InsideAbsorpVis':InsideAbsopVis,
#                       "OutsideAbsorpVis":OutsideAbsopVis,
#                       "OutsideAbsorpSolar":OutsideAbsorpSolar,
#                       "InsideAbsorpThermal":InsideAbsorpThermal,
#                       "OutsideRoughness":OutsideRoughness
#                      }
            print('\n')
            print(f'Construction system:\033[1m{name_cs}\033[0m')
            print(f'Total thickness    :{thickness} m')
            print(f'Total layers:{total_layers}')
            print(f"InsideAbsorpVis:{InsideAbsopVis}")
            print(f"OutsideAbsorpVis:{OutsideAbsopVis}")
            print(f"OutsideAbsorpSolar:{OutsideAbsorpSolar}")
            print(f"InsideAbsorpThermal:{InsideAbsorpThermal}")
            print(f"OutsideRoughness:{OutsideRoughness}")
            properties = ['NameMaterial','Conductivity', 'Density','SpecHeat', 'Thickness']
            display(cs[properties].style.hide_index())
            print('\n\n\n')
#         return all
