from prisma import Prisma

async def search_foods(query):
    prisma = Prisma()
    await prisma.connect()
    
    foods = await prisma.food.find_many(where={
        'name': {
            'contains': query,
            'mode': 'insensitive'
        }
    })
    
    await prisma.disconnect()
    return foods

async def get_food_details(food_id):
    prisma = Prisma()
    await prisma.connect()
    
    food = await prisma.food.find_unique(where={
        'id': food_id
    })
    
    await prisma.disconnect()
    return food
