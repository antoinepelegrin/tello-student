# Rempli un array des commandes correspondant a un parcours de polygone
# Divise chaque ligne droite en morceaux de 20 cm 

def polygon(commands, nb_sides, length_sides):
    sum_angles = (nb_sides - 2) * 180
    angle = 180 - int(sum_angles/nb_sides)
    
    nb_steps = int(length_sides/20)
    rm = length_sides%20
    steps = [20 for i in range(nb_steps - 1)]
    steps.append(20+rm)
    
    for i in range(nb_sides):
        for step in steps: 
            commands.append("forward " + str(step))
        
        commands.append("cw " + str(angle))
        
test = []
polygon(test, 8, 123)

print(test)

for i in test:
    print(i)
