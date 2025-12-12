import csv
from car import Car,Engine

#stays almost same as CSV 
#Car is a little better optimized
class CarRecord:
    def __init__(
        self, ID, Price, Levy, Manufacturer, Model, Prod_year, Category,
        Leather_interior, Fuel_type, Engine_volume, Mileage, Cylinders,
        Gear_box_type, Drive_wheels, Doors, Wheel, Color, Airbags
    ):
        self.ID = self._epmptyandTypeParse(ID, int)
        self.Price = self._epmptyandTypeParse(Price, float)
        self.Levy = self._epmptyandTypeParse(Levy, float)

        # string fields 
        self.Manufacturer = self._epmptyandTypeParse(Manufacturer, str)
        self.Model = self._epmptyandTypeParse(Model, str)
        self.Category = self._epmptyandTypeParse(Category, str)
        self.Leather_interior = self._epmptyandTypeParse(Leather_interior, str)
        self.Fuel_type = self._epmptyandTypeParse(Fuel_type, str)
        self.Gear_box_type = self._epmptyandTypeParse(Gear_box_type, str)
        self.Drive_wheels = self._epmptyandTypeParse(Drive_wheels, str)
        self.Doors = self._doorParse(self._epmptyandTypeParse(Doors, str))
        self.Wheel = self._epmptyandTypeParse(Wheel, str)
        self.Color = self._epmptyandTypeParse(Color, str)

        
        self.Prod_year = self._epmptyandTypeParse(Prod_year, int)

        #check for turbo if it has
        self.E_volume, self.Turbo = self._parseEngineVolume(Engine_volume)

        #remove km, then parse 
        cleaned_mileage = self._milageParse(Mileage)
        self.Mileage = self._epmptyandTypeParse(cleaned_mileage, int)

       
        self.Cylinders = self._epmptyandTypeParse(Cylinders, float)

       
        self.Airbags = self._epmptyandTypeParse(Airbags, int)

    # Helper functions

    def _epmptyandTypeParse(self, value, type):
        
        # returns None if value is '-' or empty, or the given type
        try:
            if value is None:
                return None
            
            value = str(value).strip()

            if value == "" or value == "-":
                return None

            return type(value)
        except Exception  as e:
            print(f'Error at CarRecord dashparse: {e}')
            return None

    def _parseEngineVolume(self, value):
        #some cars have turbo
        if value is None:
            return None, None

        text = str(value).strip()

        parts = text.split(" ", 1)

        volume_part = parts[0]
        turbo_part = None
        #only if it has turbo
        if len(parts) > 1:
            turbo_part = parts[1].strip().capitalize()

        
        volume = self._epmptyandTypeParse(volume_part, float)

        return volume, turbo_part

    def _milageParse(self, value):
        # return int(value.replace(" km", "").strip())
        #in case there is som unusual data
        if value is None:
            return None
        return (
            str(value)
            .replace("km", "")
            .replace("KM", "")
            .replace(" km", "")
            .replace(",", "")
            .strip()
        )

    def _doorParse(self,value):
        # excel converted strings like '02-Mar' to (2, 3)
        #also there is ">5"  treated as 2 + booth
        
        
        #doorandboot=door+1 not need all cars have boot
        # there is only 3 option Mar and May 2 or 4 doors +boot
        #>5 treated as 2 doors + booth


        if value is None:
            return None

        text = str(value).strip()

        #  ">5" 
        if text == ">5":
            return 2

        # format "02-Mar" or "04-May"
        if "-" not in text:
            return None

        left, right = text.split("-", 1)

        # Convert "02"  2
        try:
            door = int(left)
            return door
        except:
            return None





    #representation
    def __repr__(self):
        #return f"CarRecord(ID={self.ID}, Price={self.Price}, Manufacturer={self.Manufacturer}, Model={self.Model})"
        props = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"CarRecord({props})"


    
    #read csv 1 might needed to be optimaized
    def loadFromCSV(path):
        records = []

        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    record = CarRecord(
                        ID=row.get("ID"),
                        Price=row.get("Price"),
                        Levy=row.get("Levy"),
                        Manufacturer=row.get("Manufacturer"),
                        Model=row.get("Model"),
                        Prod_year=row.get("Prod. year"),
                        Category=row.get("Category"),
                        Leather_interior=row.get("Leather interior"),
                        Fuel_type=row.get("Fuel type"),
                        Engine_volume=row.get("Engine volume"),
                        Mileage=row.get("Mileage"),
                        Cylinders=row.get("Cylinders"),
                        Gear_box_type=row.get("Gear box type"),
                        Drive_wheels=row.get("Drive wheels"),
                        Doors=row.get("Doors"),
                        Wheel=row.get("Wheel"),
                        Color=row.get("Color"),
                        Airbags=row.get("Airbags")
                    )

                    records.append(record)

                except Exception as e:
                    print(f"Skipping corrupted row: {e}")

        return records
    

    
    def _toBool(self,value):
        
        #raw  to bool.
           
        if value is None:
            return None

        v = str(value).strip().lower()
        if v in ("yes", "true", "t", "1", "turbo","right-hand drive"):
            return True
        if v in ("no", "false", "0","left wheel"):
            return False

        return None


    #Create Car object
    def toCar(self):
        #turbo_flag = self._toBool(self.Turbo)

        engine = Engine(
            volume=self.E_volume,
            turbo=self._toBool(self.Turbo)
        )

        return Car(
            ID=self.ID,
            price=self.Price,
            levy=self.Levy if self.Levy is not None else 0,
            manufacturer=self.Manufacturer,
            model=self.Model,
            prod_year=self.Prod_year,
            category=self.Category,
            leather_interior= self._toBool(self.Leather_interior),
            fuel_type=self.Fuel_type,
            mileage=self.Mileage,
            cylinders=self.Cylinders,
            gear_box_type=self.Gear_box_type,
            drive_wheels=self.Drive_wheels,
            doors=self.Doors,
            right_wheel=self._toBool(self.Wheel),
            color=self.Color,
            airbags=self.Airbags,
            engine=engine
        )
    
        











