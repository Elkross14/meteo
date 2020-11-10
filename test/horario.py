from apscheduler.schedulers.background import BackgroundScheduler
import logging


def iniciar_ciclo():
    print("funciona")
    logging.warning('funciona')


logging.basicConfig(filename='example.log', filemode='w',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')
scheda = BackgroundScheduler()
# scheda.add_job(self.iniciar_ciclo, 'cron', minute='40')
scheda.add_job(iniciar_ciclo, 'interval', seconds=2)
scheda.start()


input()
