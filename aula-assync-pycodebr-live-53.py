import asyncio

async def fazerArroz():
    print('fazendo arroz')
    await asyncio.sleep(3)
    print('arroz pronto')


async def fazerFeijao():
    print('fazendo Feijao')
    await asyncio.sleep(5)
    print('Feijao pronto')


async def fazerCarne():
    print('fazendo Carne')
    await asyncio.sleep(7)
    print('Carne pronto')

async def cozinhar():
    await asyncio.gather(
        fazerArroz(),
        fazerFeijao(),
        fazerCarne()
    )
    print('Almoco pronto')

asyncio.run(cozinhar())

#explicacao
# uma funcao async no python transforma ela em uma corrotina ou seja uma funcao
# que pode ser executada em partes, de modo que quando ela encontra uma linha de codigo 
# que efetua uma rotina de I/O (exemplo consulta banco , api) o loope de eventos (libuv)
# deixa esse trecho de lado e continua a executar outros codigos e quando aquele trecho de I/O
# tiver resposta ele retoma de onde parou assim o seu sistema nao fica ocioso e nao 
# desperdiça recurso de maquina. Mas voce tem que informar no seu codigo o trecho de codigo
# que precisa fazer I/O usando a palara await

# nao confunda - paralelismo e concorrencia sao coisas diferentes. 
# um coidgo assincrono com Loop de Eventos é uma concorrencia, 
# diferente de paralelismo, que seriam diversos Loop de Eventos 
# rodando suas proprias coorotinas emm paralelo
# Concorrencia I/O Bound - Fica em 1 core e thread
# Paralelismo CPU bound - pode usar multiplos cores e threads


#live: https://www.youtube.com/watch?v=hQ-PplE8kFs