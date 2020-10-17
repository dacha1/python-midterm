import re
import urllib.request
import json

numberRegex = re.compile(r'^[+-]?(\d+((\.|\,)\d*)?|(\.|\,)\d+)([eE][+-]?\d+)?$')

currencyRegex = re.compile(r'[A-Z]{3}(?<![A-Z]{4})(?![A-Z])')

api_endpoint_USD="https://api.exchangerate-api.com/v4/latest/USD"

api_endpoint="https://api.exchangerate-api.com/v4/latest/"


def loggable(func):
    def inner(arg):
        s = func(arg)
        with open("log.txt", "a") as log_file:
            log_file.write("Input:{}\n".format(arg))
            log_file.write("Output:{}\n".format(s))
        return s
    return inner  # return the decorator function


def page_exists(page):
    try:
        urllib.request.urlopen(page)
        return True
    except:
        return False

# takes a zipcode string as a parameter
# returns location string


@loggable
def check_currency_lookup(code):
  if(page_exists(api_endpoint+code)):
    page = urllib.request.urlopen(api_endpoint_USD)
    # keep in mind the byte string needs to be decoded
    content = page.read().decode("utf-8")
    data = json.loads(content)
    rates = data['rates']

    if(code in rates.keys()):
      return True
    else:
      return False
  else:
    print("ERROR:invalid API endpoint")
    print("one or more currency codes not found")
    return False
  

def currency_lookup(code):
  currencyRegex = re.compile(r'[A-Z]{3}(?<![A-Z]{4})(?![A-Z])')
  if currencyRegex.search(code):
    return True
  else:
    print ("Invalid input {}".format(code))
    return False

  
def currency_converter(fromCurrency, toCurrency, amount):
  if(page_exists(api_endpoint+fromCurrency)):
    page = urllib.request.urlopen(api_endpoint+fromCurrency)
    content = page.read().decode("utf-8")
    data = json.loads(content)
    ratio = data['rates'][toCurrency]
    convertedAmount = ratio * float(amount)
    print("{} in {} = {} in {}".format(float(amount), fromCurrency, float(convertedAmount), toCurrency))
    return
  else:
    return


def main():
    while(True):
        amount = input("Enter amount to be converted(q to quit):")

        if(amount == 'q' or amount == 'Q'):
            print("Exiting")
            break
        elif not numberRegex.search(amount):
            print("invalid input")
            continue

        fromCurrency =  input("Enter FROM currency 3 letter code: ")
        if not currency_lookup(fromCurrency):
          continue

        toCurrency =  input("Enter To currency 3 letter code: ")
        if not currency_lookup(toCurrency):
          continue

        if (check_currency_lookup(fromCurrency) and check_currency_lookup(toCurrency)):
          currency_converter(fromCurrency, toCurrency, amount)

if __name__ == '__main__':
    main()
