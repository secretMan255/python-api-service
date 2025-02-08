from service import Service

def main():
     try:
          print('Service initialize...')
          Service()
     except Exception as err:
          print(f'Init service failed: {err}')


if __name__ == "__main__":
    main()