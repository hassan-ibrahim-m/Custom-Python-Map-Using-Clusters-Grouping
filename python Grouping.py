import pyodbc
import pandas as pd
import warnings

import sqlalchemy
pd.options.mode.chained_assignment = None  # default='warn'
conn = pyodbc.connect('Driver={SQL Server};' 'Server=xx.xx.xxx.xxx;' 'Database=XXXX;' 'Trusted_Connection=yes;' 'ID=sa;' 'Password=NTRA@@2020;')

# QUERY
query = '''
SELECT q.[Datekey],[Cluster Name] as ClusterName, operator, MeasureID, Value,
case when measureID = 1 and value > 2 then 1
when measureID = 2 and value > 2 then 1
when measureID = 3 and value > 3 then 1 when
measureID = 5 and value > 2 then 1
when measureID = 6 and value < 5 then 1
when measureID = 7 and value < 2 then 1
else 0
end as isViolated
FROM [NTRA].[Quality].[FT_Quality] q
left join
DimDate d on q.[Datekey] = d.DateKey
left join
[Quality].[DimEntCluster] c on q.ClusterID = c.ID
where measureID in (1,2,3,5,6,7)'''
# QUERY
warnings.filterwarnings("ignore")
cursor = conn.cursor()
df = pd.read_sql_query(query, conn)
conn.close()

df['indx'] = df['Datekey']
df = df.set_index('indx')
df['consViolations'] = 0
ClustersList = df['ClusterName'].unique()
OperatorsList = df['operator'].unique()
MeasuresList = df['MeasureID'].unique()
ClusterGrouped = df.groupby(df.ClusterName)
output = pd.DataFrame(columns = ['Datekey', 'ClusterName', 'MeasureID', 'Value', 'operator', 'isViolated', 'consViolations'])
for cluster in ClustersList:
    clusterGrouped_1 = ClusterGrouped.get_group(cluster)
    MeasureGrouped = clusterGrouped_1.groupby(clusterGrouped_1.MeasureID)
    for measure in MeasuresList:
        measureGrouped_1 = MeasureGrouped.get_group(measure)
        OperatorGrouped = measureGrouped_1.groupby(measureGrouped_1.operator)
        for operator in OperatorsList:
            operatorGrouped_1 = OperatorGrouped.get_group(operator)
            consViolations = 0
            operatorGrouped_1.sort_values(by="Datekey", inplace=True)
            for index, row in operatorGrouped_1.iterrows():
                if row['isViolated'] == 1:
                    consViolations += 1
                    operatorGrouped_1.loc[row['Datekey'], 'consViolations'] = consViolations
                else:
                    consViolations = 0
                    operatorGrouped_1.loc[row['Datekey'], 'consViolations'] = consViolations
            warnings.filterwarnings("ignore")
            output = output.append(operatorGrouped_1)

print(output)