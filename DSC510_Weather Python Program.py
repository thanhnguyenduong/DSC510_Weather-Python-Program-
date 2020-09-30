"""
File: Assignment_12.1.py
Author: Thanh Nguyen-Duong
Date: 11/11/19
Course: DSC 510-T304 Fall 2019
Assignment: 12.1
Desc: This program prompts user for zip code or city name to obtain weather forecast information from OpenWeatherMap
Usage: Program displays options to allow user to continue until user ends the program.
       Prompts user for zip code or city name to obtain weather forecast information from OpenWeatherMap.
       Display requested weather forecast information as current conditions and 5-day forecast plots.
       Ensure connection to webservice is successful by display a message to user.
"""
import requests
import datetime
from matplotlib.pyplot import show, subplots
from matplotlib import dates

class WeatherAPI:
    """
    Weather class is used to pull weather data for zip codes or cities from OpenWeatherMap using API key
    """
    # api_key to request the weather
    api_key = 'dc2809eb0ce059ca5e268478a7919ae0'
    # base url to request the data through the api
    base_url = 'http://api.openweathermap.org/data/2.5/'

    # initiate the weather class
    def __init__(self):
        self.country = 'us'
        self._zipCode = 0
        self._city = ''
        self._state = ''
        self._units = 'imperial'
        self._data_weather = {}  # data dictionary for the current weather forecast
        self._data_forecast = {}  # data for the five day forecast

    # setting all decorators and setters for weather class
    @property
    def zipCode(self):
        return self._zipCode

    @zipCode.setter
    def zipCode(self, _zipCode):
        self._zipCode = _zipCode

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, _city):
        self._city = _city

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, _state):
        self._state = _state

    @property
    def city_state(self):
        return '{},{}'.format(self.city, self.state)

    @city_state.setter
    def city_state(self, city_state):
        city, state = city_state.split(",")
        # lower to keep url consistent
        self.city = city.lower()
        self.state = state.lower()

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, _units):
        self._units = _units

    @property
    def data_weather(self):
        return self._data_weather

    @data_weather.setter
    def data_weather(self, _data_weather):
        self._data_weather = _data_weather

    @property
    def data_forecast(self):
        return self._data_forecast

    @data_forecast.setter
    def data_forecast(self, _data_forecast):
        self._data_forecast = _data_forecast

    # call weather data using zip code
    def getZipCodeData(self):
        try:
            self.getWeatherZip()
            self.getForecastZipCode()
            # Ensure request and connection was successful
            print('Connection was a success!')
            # print if connection is successful
            self.printWeather()
        except:
            print('Please enter a valid zip code.')  # exception if invalid zip code

    # call weather data by city code
    def getCityData(self):
        try:
            self.getWeatherCity()
            self.getForecastCity()
            # Ensure request and connection was successful
            print('Connection was a success!')
            # print if connection is successful
            self.printWeather()
        except:
            print('Please enter valid city information.')  # exception if invalid city

    # call for current weather conditions
    def getWeatherCity(self):
        try:
            # request data from website
            response = requests.get(
                '{0}weather?q={1},{2}&units={3}&appid={4}'.format(self.base_url, self.city_state, self.country,
                                                                  self.units, self.api_key))
            # append current weather conditions into weather data dictionary
            assert int(response.json()['cod']) < 400
            self.data_weather = response.json()
            self.transformWeatherData()
            # flag error if issues with request and stop program
        except AssertionError:
            return AssertionError
        except requests.exceptions.RequestException as e:
            print(e)
            return e

    # Call for weather forecast using city
    def getForecastCity(self):
        try:
            # request data from website
            response = requests.get(
                '{0}forecast?q={1},{2}&units={3}&appid={4}'.format(self.base_url, self.city_state, self.country,
                                                                   self.units, self.api_key))
            # append 5 day forecast conditions into forecast data dictionary
            assert int(response.json()['cod']) < 400
            self.data_forecast = response.json()
            self.transformForecastData()
            # flag error if issues with request and stop program
        except AssertionError:
            return AssertionError
        except requests.exceptions.RequestException as e:
            print(e)
            return e

    # call for current weather conditions using zip code
    def getWeatherZip(self):
        try:
            # request data from website
            response = requests.get(
                '{0}weather?zip={1},{2}&units={3}&appid={4}'.format(self.base_url, self.zipCode, self.country,
                                                                    self.units, self.api_key))
            # insert current weather conditions into weather data dictionary
            assert int(response.json()['cod']) < 400
            self.data_weather = response.json()
            self.transformWeatherData()
            # flag error if issues with request and stop program
        except AssertionError:
            return AssertionError
        except requests.exceptions.RequestException as e:
            print(e)
            return e

    # call for 5-day forecast weather using zip code
    def getForecastZipCode(self):
        try:
            # request data from website
            response = requests.get(
                '{0}forecast?zip={1},{2}&units={3}&appid={4}'.format(self.base_url, self.zipCode, self.country,
                                                                     self.units, self.api_key))
            # append 5 day forecast conditions into forecast data dictionary
            assert int(response.json()['cod']) < 400
            self.data_forecast = response.json()
            self.transformForecastData()
            # flag error if issues with request and stop program
        except AssertionError:
            return AssertionError

    def transformWeatherData(self):
        # creating timezone and current date to display weather information
        timezone = self.data_weather['timezone']
        datetime.datetime.utcfromtimestamp(self.data_weather['dt'] + self.data_weather['timezone'])
        # get the weather description
        desc = self.data_weather['weather'][0]['description']
        # current temp
        temp = self.data_weather['main']['temp']
        # current humidity
        humidity = self.data_weather['main']['humidity']
        # sunrise and sunset time
        sunrise = datetime.datetime.utcfromtimestamp(self.data_weather['sys']['sunrise'] + timezone)
        sunset = current_date = datetime.datetime.utcfromtimestamp(self.data_weather['sys']['sunset'] + timezone)
        # rain, snow and wind information
        try:
            rain = '{} mm'.format(self.data_weather['rain']['1h'])
        except:
            rain = '0'
        try:
            snow = '{} mm'.format(self.data_weather['snow']['1h'])
        except:
            snow = '0'
        try:
            wind = '{} mph {}'.format(self.data_weather['wind']['speed'],
                                      degreesToCardinal(self.data_weather['wind']['deg']))
        except:
            wind = '0 mph'
        # update data_weather, to better access what we need
        self.data_weather = {'current_date': current_date, 'desc': desc, 'temp': temp, 'humidity': humidity,
                             'rain': rain, 'snow': snow, 'wind': wind, 'sunrise': sunrise, 'sunset': sunset}

    # this is used to transform forecast dates
    def transformForecastData(self):
        # constructing lists
        Date = []
        temps = []
        humidity = []
        clouds = []
        rain = []
        snow = []
        # timezone and date used to display current time in place of request
        timezone = self.data_forecast['city']['timezone']
        for i in self.data_forecast['list']:
            # date and time used to plot graph
            Date.append(datetime.datetime.utcfromtimestamp(i['dt'] + timezone))
            # storing temperatures, humidity, clouds
            temps.append(i['main']['temp'])
            humidity.append(i['main']['humidity'])
            clouds.append(i['clouds']['all'])
            try:
                rain.append(i['rain']['3h'])
            except:
                rain.append(0)
            try:
                snow.append(i['snow']['3h'])
            except:
                snow.append(0)
            # try used to make sure we capture a data point for each list so it matches dates, set to zero if it doesn't exist
        # update data_forecast for plotting graphs
        self.data_forecast = {'dates': Date, 'temps': temps, 'humidity': humidity, 'rain': rain, 'snow': snow}

    # used to pull the minimum time from dates
    @staticmethod
    def getMinHour(inList):
        # construct list
        hour = []
        # try used in case it is called and no data sent or bad data is sent
        try:
            for i in inList:
                # insert hour values to see the min
                hour.append(i.strftime("%H"))
            return int(min(hour))
        except:
            # inform user data is bad
            print('error: bad dates entered from list')
            # used to flag an error that there is no data
            return AssertionError

    # print the 5 day forecast using graphs - temperature
    def printForecastGraph(self):
        # use x and y values
        x = self.data_forecast['dates']
        y = self.data_forecast['temps']
        # draw line for when the dates start and end
        min_x = self.getMinHour(x)

        # setup graph
        fig6, ax = subplots()
        # naming of the graph and axis
        ax.set_title("5-Day Forecast")
        ax.set_xlabel("Day")
        ax.set_ylabel("Temperature (F)")
        # setup graph to plot
        ax.plot(x, y)
        # start both axis at 0
        ax.margins(0)
        # create vertical line at midnight for each graph
        for i in x:
            # compare hour to min
            if int(i.strftime("%H")) == int(min_x):
                ax.axvline(i, color='g')
        # set the Mon, Tues,... at the 12 pm position
        ax.xaxis.set_major_locator(dates.HourLocator(byhour=12))
        # format dates to days of the week
        ax.xaxis.set_major_formatter(dates.DateFormatter("%a"))
        # set grid lines
        ax.grid()
        show()

    # print the 5-day forecast - humidity
    def printHumidity(self):
        # use x and y values
        x = self.data_forecast['dates']
        y = self.data_forecast['humidity']
        # draw line for when the dates start and end
        min_x = self.getMinHour(x)

        # setup graph
        fig6, ax = subplots()
        # naming of the graph and axis
        ax.set_title("5-Day Forecast: Humidity")
        ax.set_xlabel("Day")
        ax.set_ylabel("% Humidity")
        # setup graph to plo
        ax.plot(x, y, color='r')
        # start both axis at 0
        ax.margins(0)
        # create vertical line at midnight for each graph
        for i in x:
            # compare hour to min
            if int(i.strftime("%H")) == int(min_x):
                ax.axvline(i, color='g')
        # set the Mon, Tues,... at the 12 pm position
        ax.xaxis.set_major_locator(dates.HourLocator(byhour=12))
        # format dates to Mon, Tues, Wed, etc
        ax.xaxis.set_major_formatter(dates.DateFormatter("%a"))
        # set grid lines
        ax.grid()
        show()

    # print the 5-day forecast - precipitation
    def printPrecipitation(self):
        # use x and y values
        x = self.data_forecast['dates']
        y_rain = self.data_forecast['rain']
        y_snow = self.data_forecast['snow']
        # draw line for when the dates start and end
        min_x = self.getMinHour(x)

        # setup graph
        fig6, ax = subplots()
        # naming of the graph and axis
        ax.set_title("5 Day Forecast:Precipitation")
        ax.set_xlabel("Day")
        ax.set_ylabel("Precipitation (inches)")
        # setup graph to plot
        ax.plot(x, y_rain, color='blue', label='Rain')
        ax.plot(x, y_snow, color='yellow', label='Snow')
        ax.legend()

        # start both axis at 0
        ax.margins(0)
        # create vertical line at midnight for each graph
        for i in x:
            # compare hour to min
            if int(i.strftime("%H")) == int(min_x):
                ax.axvline(i, color='g')
        # set the Mon, Tues,... at the 12 pm position
        ax.xaxis.set_major_locator(dates.HourLocator(byhour=12))
        # format dates to Mon, Tues, Wed, etc
        ax.xaxis.set_major_formatter(dates.DateFormatter("%a"))
        # set grid lines
        ax.grid()
        show()

    # used to display the weather for the user
    def printWeather(self):
        # print current conditions
        print(
            '\n\nCurrent weather for {0}:\n{1}, temperature: {2} F\nWind: {3} \nHumidity: {4} % \nRain: {5} \nSnow: {6} \nSunrise: {7}\nSunset: {8}'.format(
                self.data_weather['current_date'].strftime("%x"), self.data_weather['desc'], self.data_weather['temp'],
                self.data_weather['wind'], self.data_weather['humidity'], self.data_weather['rain'],
                self.data_weather['snow'], self.data_weather['sunrise'].strftime("%I:%M:%S %p"),
                self.data_weather['sunset'].strftime("%I:%M:%S %p")))
        # print 5-day forecasts
        self.printForecastGraph()
        self.printHumidity()
        self.printPrecipitation()


# degree coordination for wind
def degreesToCardinal(deg):
    direction = {"N": [337.5, 22.5], "NE": [22.5, 67.5], "E": [67.5, 112.5], "SE": [112.5, 157.5],
                 "S": [157.5, 202.5], "SW": [202.5, 247.5], "W": [247.5, 292.5], "NW": [292.5, 337.5]}
    for key, val in direction.items():
        if val[0] <= deg < val[1]:
            return key


def main():
    # this is the main program that control all functions and cycle the program until user ends
    isContinue = True
    # prompts user to input city or zip code
    promptBegin = 'Welcome user,\nThis program allows you to see the forecast of the desired city by enter the zip code or a city and state.' \
                  '\nThe data will generate current weather conditions and 5-day forecast plots.' \
                  '\n"q" to end the program.'
    promptFormatting = '(Format: zip code= 94024 OR San Jose, CA)'
    promptContinue = '\nenter a zip code or City, State.{}.'.format(promptFormatting)
    promptAssert = '\nThe zip code must be a number greater than 0.'
    promptError = '\nPlease try again, make sure to include a comma in between city and state.'
    promptExit = '\nHope this program was helpful, have a nice day!'
    print(promptBegin)
    # continue to enter data until the user hits'q'
    while isContinue:
        user_input = input(promptContinue)
        weather = WeatherAPI()
        try:
            if user_input.lower() == 'q':
                print(promptExit)
                isContinue = False
            else:
                if ',' in user_input:
                    weather.city_state = user_input
                    weather.getCityData()

                else:
                    user_input = int(user_input)
                    assert user_input > 0
                    weather.zipCode = user_input
                    weather.getZipCodeData()
        except AssertionError:
            print(promptAssert)
        except:
            print(promptError)


if __name__ == "__main__":
    main()
