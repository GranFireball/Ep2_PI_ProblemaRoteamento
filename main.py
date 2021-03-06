import random
import math

def create_data_model():
    data = {}
    data['matriz_distancia'] = [
        [
            0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
            468, 776, 662
        ],
        [
            548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
            1016, 868, 1210
        ],
        [
            776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
            1130, 788, 1552, 754
        ],
        [
            696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
            1164, 560, 1358
        ],
        [
            582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
            1050, 674, 1244
        ],
        [
            274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
            514, 1050, 708
        ],
        [
            502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
            514, 1278, 480
        ],
        [
            194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
            662, 742, 856
        ],
        [
            308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
            320, 1084, 514
        ],
        [
            194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
            274, 810, 468
        ],
        [
            536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
            730, 388, 1152, 354
        ],
        [
            502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
            308, 650, 274, 844
        ],
        [
            388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
            536, 388, 730
        ],
        [
            354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
            342, 422, 536
        ],
        [
            468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
            342, 0, 764, 194
        ],
        [
            776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
            388, 422, 764, 0, 798
        ],
        [
            662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
            536, 194, 798, 0
        ],
    ]
    data['num_vehicles'] = 4
    data['depot'] = 0
    return data
data = create_data_model()

# hiperpar??metros
tamanho_populacao = 100
tx_mutacao = 0.1
tx_crossover = 0.15
tx_tragedia = 0.05
#geracoes_max = 100_000
geracoes_max = 2_000
geracoes_tragedia = 100


def fitness(individuo):
  score = 0
  for trajeto_van in individuo:
    for i in range(len(trajeto_van)-1):
      score += data["matriz_distancia"][trajeto_van[i]][trajeto_van[i+1]]
  return score

def gerar_individuo():
  individuo = []
  qntd_trajetos = len(data["matriz_distancia"])
  trajetos = list(range(qntd_trajetos))
  trajetos.pop(data["depot"])
  random.shuffle(trajetos)

  for qntd_vans in range(data["num_vehicles"], 0, -1):
    van:list = []
    # arredonda a divis??o da quantidade de trajetos pela quantidade de vans restantes
    qntd_trajetos_associados = round(len(trajetos)/qntd_vans)
    van.append(0)

    for trajetos_index in range(qntd_trajetos_associados-1, -1, -1):
      van.append(trajetos.pop(trajetos_index))
    van.append(0)
    individuo.append(van)
  return individuo
  
# retorna populacao mutada com uma taxa
def mutacao(populacao):
  populacao_escolhida = random.choices(populacao, k=math.ceil(tx_mutacao*len(populacao)))
  return [mutacao_DuplaTroca(individuo) for individuo in populacao_escolhida]
  #return [mutacao_Reversao(individuo) for individuo in populacao_escolhida]

def mutacao_DuplaTroca(individuo):
  novo_individuo = list(individuo)
  for i in individuo:
    index = random.randint(0, len(i) - 3)
    index2 = index + 2  
    aux = i[index]
    i[index] = i[index2]
    i[index2] = aux
  return novo_individuo

def mutacao_Reversao(individuo):
  novo_individuo = list(individuo)
  aux = [0] * 3
  for i in individuo:     
    for a in range(0,3):
      aux[a] = i[a]
    for j in range(0,3):
      i[j] = i[j+3]
    for k in range(0,3):
      i[k+3] = aux[k]
  return novo_individuo

def crossover(populacao):   
  qtd = tx_crossover*len(populacao)
  populacao_crossover = []
  populacao_escolhida = random.choices(populacao, k=math.ceil(qtd))
  for i in range(len(populacao_escolhida) - 1):
    for j in range(i+1, len(populacao_escolhida)):
      ind1 = populacao_escolhida[i]
      ind2 = populacao_escolhida[j]

      index = random.randint(0, len(populacao_escolhida) - 1)
      populacao_crossover.append(ind1[0:index] + ind2[index:])
      populacao_crossover.append(ind2[0:index] + ind1[index:])

  return populacao_crossover

# escolhe os indiv??duos mais aptos
def selecao_com_tragedia(populacao, geracao):
  nova_populacao = sorted(populacao, key=fitness, reverse=True)
  if (geracao % geracoes_tragedia == 0):
    tamanho_tragedia = math.ceil(tamanho_populacao*tx_tragedia)
    novos_individuos = [gerar_individuo() for _ in range(0, tamanho_populacao - tamanho_tragedia)]
    return nova_populacao[0:tamanho_tragedia] + novos_individuos
  else:
    return nova_populacao[0:tamanho_populacao]

def selecao(populacao, geracao):
  nova_populacao = sorted(populacao, key=fitness, reverse=True)
  return nova_populacao[0:tamanho_populacao]

populacao = [gerar_individuo() for _ in range(0, tamanho_populacao)]
# ordernar lista
populacao = sorted(populacao, key=fitness)
geracao = 0
while geracao < geracoes_max:
  geracao += 1
  populacao_mutada = mutacao(populacao)
  populacao_crossover = crossover(populacao)

  if(geracao > 1000):
    populacao = selecao_com_tragedia(populacao_mutada + populacao + populacao_crossover, geracao)
  else:
    populacao = selecao(populacao_mutada + populacao + populacao_crossover, geracao)

  if geracao % 100 == 0 or (geracao % 10 == 0 and geracao < 100):
    print("---------------- GERA????O: " + str(geracao)+ " ----------------")
    print(populacao[0])
    print("Dist??ncia percorrida: " + str(fitness(populacao[0])))

#Sa??da Esperada
for i, trajeto_van in enumerate(populacao[0]):
  print("Van " + str((i + 1)))
  trajeto_sem_deposito = [str(numero) for numero in trajeto_van]
  trajeto_sem_deposito = trajeto_sem_deposito[1:len(trajeto_sem_deposito) - 1]
  score = 0
  for j in range(len(trajeto_van) - 1):
    score += data["matriz_distancia"][trajeto_van[j]][trajeto_van[j+1]]
  print("Dist??ncia percorrida pela van ", i + 1, ": ", score, '\n')

print("Dist??ncia percorrida: " + str(fitness(populacao[0])))