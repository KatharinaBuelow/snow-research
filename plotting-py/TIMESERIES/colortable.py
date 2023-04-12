# python 
from cmcrameri import cm

def colortable(key):
  # Estelle dictionary fuer die plotfarben
    design_tab = {'palette':{'rcp85':[cm.lajolla(0.5),cm.lajolla(0.7),cm.lajolla(0.9)],
                             'rcp45':[cm.lajolla(0.1),cm.lajolla(0.3),cm.lajolla(0.5)],
                             'rcp26':[cm.roma(0.70),cm.roma(0.8),cm.roma(1.0)]},
                  'colors':{'1971-2000_rcp85':cm.lajolla(0.5),
                            '2021-2050_rcp85':cm.lajolla(0.7),
                            '2069-2098_rcp85':cm.lajolla(0.9),
                            '1971-2000_rcp45':cm.lajolla(0.1),
                            '2021-2050_rcp45':cm.lajolla(0.3),
                            '2069-2098_rcp45':cm.lajolla(0.5),
                            '1971-2000_rcp26':cm.roma(0.7),
                            '2021-2050_rcp26':cm.roma(0.8),
                            '2069-2098_rcp26':cm.roma(1.0)},
                  'colrcp':  {'rcp85':cm.lajolla(0.7),
                            'rcp45':cm.lajolla(0.3),
                            'rcp26':cm.roma(0.8)}
                  }
    
    
