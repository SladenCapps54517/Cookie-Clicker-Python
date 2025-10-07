import time
import json
import os
import threading




SAVE_FILE = "cookie_clicker_save.json"




class StoreItem:
  def __init__(self, name, cost, base_cps, count=0, perk_level=0, perk_cost=100000000):
      self.name = name
      self.cost = cost
      self.base_cps = base_cps
      self.count = count
      self.perk_level = perk_level
      self.perk_cost = perk_cost




  def current_cps(self):
      return self.base_cps * (1 + 0.15 * self.perk_level)




  def total_cps(self):
      return self.current_cps() * self.count




  def to_dict(self):
      return {
          "name": self.name,
          "cost": self.cost,
          "base_cps": self.base_cps,
          "count": self.count,
          "perk_level": self.perk_level,
          "perk_cost": self.perk_cost
      }




  @staticmethod
  def from_dict(data):
      return StoreItem(
          data["name"],
          data["cost"],
          data["base_cps"],
          data["count"],
          data["perk_level"],
          data["perk_cost"]
      )




  def increase_cost(self):
      self.cost = round(self.cost * 1.08)




  def increase_perk_cost(self):
      self.perk_cost = round(self.perk_cost * 1.25)




class CookieClicker:
  def __init__(self):
      self.total_clicks = 0
      self.click_power = 1
      self.click_power_perk_cost = 50000
      self.items = [
          StoreItem("Clicker", 10, 1/10),
          StoreItem("Grandma", 100, 1),
          StoreItem("CookieFarm", 1000, 50),
          StoreItem("CookieMine", 20000, 100),
          StoreItem("CookieBank", 150000, 5000),
          StoreItem("CookieTemple", 1000000, 30000),
          StoreItem("WizzardTower", 10000000, 100000),
          StoreItem("Shipment", 100000000, 550000),
          StoreItem("AlchemyLab", 500000000, 10000000),
          StoreItem("Portal", 30000000000, 1000000000),
          StoreItem("TimeMachine", 1000000000000, 9500000000),
          StoreItem("Prism", 900000000000, 20000000000)
      ]
      self.recalculate_cps()




  def recalculate_cps(self):
      self.total_cps = sum(item.total_cps() for item in self.items)




  def click_cookie(self):
      self.total_clicks += self.click_power
      print(f"\n🍪 Clicked! +{self.click_power} clicks. Total Cookies: {self.total_clicks}")




  def buy_item(self, item_name, amount=1):
      for item in self.items:
          if item.name.lower() == item_name.lower():
              total_cost = 0
              for _ in range(amount):
                  total_cost += item.cost
                  item.increase_cost()
              if self.total_clicks >= total_cost:
                  self.total_clicks -= total_cost
                  item.count += amount
                  self.recalculate_cps()
                  print(f"\n✅ Bought {amount} {item.name}(s)! You now own {item.count}. New cost: {item.cost}")
              else:
                  print(f"\n❌ Not enough clicks. Needed: {total_cost}, You have: {self.total_clicks}")
              return
      print("\n❌ Item not found.")




  def buy_perk(self, item_name):
      for item in self.items:
          if item.name.lower() == item_name.lower():
              if self.total_clicks >= item.perk_cost:
                  self.total_clicks -= item.perk_cost
                  item.perk_level += 1
                  item.increase_perk_cost()
                  self.recalculate_cps()
                  print(f"\n✨ Perk upgraded for {item.name}! CPS boosted by 15%. New perk cost: {item.perk_cost}")
              else:
                  print(f"\n❌ Not enough clicks for perk. Needed: {item.perk_cost}, You have: {self.total_clicks}")
              return
      print("\n❌ Item not found.")




  def buy_click_power_perk(self):
      if self.total_clicks >= self.click_power_perk_cost:
          self.total_clicks -= self.click_power_perk_cost
          self.click_power *= 2
          self.click_power_perk_cost = round(self.click_power_perk_cost * 1.5)
          print(f"\n💥 Click Power doubled! New power: {self.click_power}. Next perk cost: {self.click_power_perk_cost}")
      else:
          print(f"\n❌ Not enough clicks for Click Power perk. Needed: {self.click_power_perk_cost}, You have: {self.total_clicks}")




  def generate_passive_clicks(self, interval=1.0):
      self.total_clicks += self.total_cps * interval




  def show_store(self):
      print("\n🛒 Store Items:")
      for item in self.items:
          print(f"- {item.name}: Cost = {item.cost}, Owned = {item.count}, CPS = {item.current_cps():.2f}, Total CPS = {item.total_cps():.2f}, Perk Level = {item.perk_level}, Perk Cost = {item.perk_cost}")
      print(f"\n⚡ Click Power: {self.click_power}, Perk Cost: {self.click_power_perk_cost}")
      print(f"📈 Total CPS: {self.total_cps:.2f}")




  def display_status(self):
      print(f"\n📊 Status: Total Clicks = {round(self.total_clicks, 2)}, Click Power = {self.click_power}, Total CPS = {round(self.total_cps, 2)}")




  def save_game(self):
      data = {
          "total_clicks": self.total_clicks,
          "click_power": self.click_power,
          "click_power_perk_cost": self.click_power_perk_cost,
          "items": [item.to_dict() for item in self.items]
      }
      with open(SAVE_FILE, "w") as f:
          json.dump(data, f)
      print("\n💾 Game saved!")




  def load_game(self):
      if not os.path.exists(SAVE_FILE):
          print("\n⚠️ No saved game found.")
          return
      with open(SAVE_FILE, "r") as f:
          data = json.load(f)
      self.total_clicks = data["total_clicks"]
      self.click_power = data.get("click_power", 1)
      self.click_power_perk_cost = data.get("click_power_perk_cost", 50000)
      self.items = [StoreItem.from_dict(item) for item in data["items"]]
      self.recalculate_cps()
      print("\n📂 Game loaded!")




  def new_game(self):
      self.__init__()
      print("\n🆕 New game started!")




  def start_realtime_updates(self):
      def update_loop():
          interval = 0.01
          while True:
              time.sleep(interval)
              self.generate_passive_clicks(interval)
              try:
                  print(f"\r📊 Real-Time → Clicks: {round(self.total_clicks, 2)} | CPS: {round(self.total_cps, 2)}", end="")
              except Exception:
                  pass
      thread = threading.Thread(target=update_loop, daemon=True)
      thread.start()




def main():
  game = CookieClicker()
  game.start_realtime_updates()
  print("\n🍪 Welcome to Cookie Clicker!")
  print("Commands: 'click' or 'c', 'buy [item] [amount]' or 'b [item] [amount]', 'perk [item]', 'clickperk', 'store' or 's', 'wait' or 'w', 'save' or 'v', 'load' or 'l', 'new' or 'n', 'exit' or 'x'.")




  while True:
      try:
          command = input("\nEnter command: ").strip().lower()
      except EOFError:
          break




      if command in ["click", "c"]:
          game.click_cookie()
      elif command.startswith("buy ") or command.startswith("b "):
          parts = command.split()
          if len(parts) >= 3 and parts[2].isdigit():
              item_name = parts[1]
              amount = int(parts[2])
          else:
              item_name = parts[1]
              amount = 1
          game.buy_item(item_name, amount)
      elif command.startswith("perk "):
          item_name = command[5:]
          game.buy_perk(item_name)
      elif command == "clickperk":
          game.buy_click_power_perk()
      elif command in ["store", "s"]:
          game.show_store()
      elif command in ["wait", "w"]:
          print("\n⏳ Waiting 5 seconds to generate passive clicks...")
          time.sleep(5)
          game.generate_passive_clicks(5)
      elif command in ["save", "v"]:
          game.save_game()
      elif command in ["load", "l"]:
           game.load_game()
      elif command in ["new", "n"]:
          game.new_game()
      elif command in ["exit", "x"]:
          print("\n👋 Thanks for playing! Final Clicks:", round(game.total_clicks, 2))
          break
      else:
          print("\n❓ Unknown command. Try 'c', 'b [item] [amount]', 'perk [item]', 'clickperk', 's', 'w', 'v', 'l', 'n', or 'x'.")




if __name__ == "__main__":
  main()