import boto3

def readfile():
    file = input('enter a filename here: ')
    readfile = open(file, 'r')
    txt = readfile.read()
    return txt

translate = boto3.client(service_name='translate', region_name='us-west-2', use_ssl=True)
result = translate.translate_text(Text=readfile(), 
            SourceLanguageCode="en", TargetLanguageCode="de")
# print('TranslatedText: ' + result.get('TranslatedText'))
# print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
# print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))

targetlanguage = result.get('TargetLanguageCode')