import { ClientOptions, Pool } from 'packages/postgres@v0.17.0/mod.ts'
import { load } from 'deps/lib.ts'

const env = await load()

const MODE = env['MODE']
const postgresSQLDev: ClientOptions = {
  user: env['DB_USER'],
  database: env['DB_NAME'],
  hostname: env['DB_HOSTNAME'],
  port: env['DB_PORT'],
  password: env['DB_PASSWORD'],
}
const posgresSQLProd = env['DB_DEPLOY']
const connectToPostgreSQL = MODE === 'dev' ? postgresSQLDev : posgresSQLProd

const client = new Pool(connectToPostgreSQL, 3, true)
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))
let attempts = 0

const isConectedToPostgres = await client.connect()

while (attempts < 5) {
  try {
    console.log('🐳 Connecting to postgres...')
    console.log('🚀 Connection succesfuly to postgres')
    break
  } catch (error) {
    console.log('❌ Obtuviste un problema a conectarte a postgres')
    console.log('📕 PROBLEMA: ', (error as Error).message)
    console.log('🐳 Intentando nuevamente, conectando...')
    await sleep(5000)
    attempts++
  } finally {
    isConectedToPostgres.release()
  }
}

export default isConectedToPostgres
