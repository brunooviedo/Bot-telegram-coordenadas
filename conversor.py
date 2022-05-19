import math
import simplekml
import utm
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    MessageHandler, Filters
    
#CONSTANTES UTM A MINA
constante_1 = 1.31415E-05
constante_2	= 1.00087683
constante_3	= -476994.037
constante_4	= -7214453.535
#CONSTANTES MINA UTM
constante_5 = -1.31415E-05
constante_6 = 0.999123937
constante_7 = 476481.435
constante_8 = 7208139.49

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="hola soy un bot para convetir coordenas UTM A MINA Y VICEVERSA"
    )
    
start_handler = CommandHandler('start', start)

def help_command(update, context: CallbackContext) -> None:
    update.message.reply_text("/mina <Coordenada Este> <Coordenada Norte> \n /utm <Coordenada Este> <Coordenada Norte>")

    
help_handler = CommandHandler('ayuda', help_command)   

def convertir_utm(update, context: CallbackContext) -> None:
    try:
        chat_id = update.message.chat_id
        a = round(constante_6*float(context.args[0])*math.cos(constante_5)+constante_6*float(context.args[1])*math.sin(constante_5)+constante_7,3)
        b = round(constante_6*float(context.args[1])*math.cos(constante_5)-constante_6*float(context.args[0])*math.sin(constante_5)+constante_8,3)
        update.message.reply_text(f'La conversion ES :  ESTE  {a}  NORTE  {b} \n \n Se genero el siguiente archivo Kml')
        
        convert = utm.to_latlon(a, b, 19, 'k')

        longitud = convert[1]
        latitud = convert[0]

        kml = simplekml.Kml()
        kml.newpoint(name="coordenadas", coords=[(longitud,latitud)])
        kml.save("utm.kml")
        document = open('utm.kml', 'rb')
        context.bot.send_document(chat_id, document)
    except:
        update.message.reply_text('Lo siento, no logro entender, intenta nuevamente')
        
utm_handler = CommandHandler('utm', convertir_utm)

def convertir_mina(update, context: CallbackContext) -> None:
    try:
        a = round(constante_2*float(context.args[0])*math.cos(constante_1)+constante_2*float(context.args[1])*math.sin(constante_1)+constante_3,3)
        b = round(constante_2*float(context.args[1])*math.cos(constante_1)-constante_2*float(context.args[0])*math.sin(constante_1)+constante_4,3)
        update.message.reply_text(f'La conversion ES :  ESTE  {a}  NORTE  {b} ')
               
        
    except:
        update.message.reply_text('Lo siento, no logro entender')
        
mina_handler = CommandHandler('mina', convertir_mina)
        

def main():
    updater = Updater("#####################################") #token telegram
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(mina_handler)
    dispatcher.add_handler(utm_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
