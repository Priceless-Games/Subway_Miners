import random
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Dictionary to hold the game state for each user
game_state = {}
leaderboard = {}

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    game_state[user_id] = {
        'position': 1,
        'obstacles': [],
        'score': 0,
        'level': 1,
        'power_up': False,
        'turns_left_power_up': 0,
        'currency': 0
    }
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Subway Miners!\nUse /left, /right, /jump to play. Collect power-ups by avoiding obstacles!")

def move_left(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in game_state:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please start the game using /start.")
        return
    if game_state[user_id]['position'] > 1:
        game_state[user_id]['position'] -= 1
    update_game(update, context)

def move_right(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in game_state:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please start the game using /start.")
        return
    if game_state[user_id]['position'] < 3:
        game_state[user_id]['position'] += 1
    update_game(update, context)

def jump(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in game_state:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please start the game using /start.")
        return
    # Jump avoids the next obstacle
    if game_state[user_id]['obstacles']:
        game_state[user_id]['obstacles'].pop(0)
    update_game(update, context)

def update_game(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    position = game_state[user_id]['position']
    obstacles = game_state[user_id]['obstacles']
    power_up = game_state[user_id]['power_up']
    turns_left_power_up = game_state[user_id]['turns_left_power_up']
    
    # Add a new obstacle or power-up with some probability
    if random.random() < 0.3:
        if random.random() < 0.1:
            obstacles.append('P')
        else:
            obstacles.append(random.randint(1, 3))
    
    # Check for collision
    if obstacles and obstacles[0] == position:
        if power_up:
            game_state[user_id]['obstacles'].pop(0)
            game_state[user_id]['power_up'] = False
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Game Over! Your score: {game_state[user_id]['score']}")
            update_leaderboard(user_id)
            game_state.pop(user_id)
            return
    
    # Check for power-up collection
    if obstacles and obstacles[0] == 'P':
        game_state[user_id]['power_up'] = True
        game_state[user_id]['turns_left_power_up'] = 5
        obstacles.pop(0)
    
    # Update power-up state
    if power_up:
        game_state[user_id]['turns_left_power_up'] -= 1
        if game_state[user_id]['turns_left_power_up'] == 0:
            game_state[user_id]['power_up'] = False
    
    # Update score and level
    game_state[user_id]['score'] += 1
    if game_state[user_id]['score'] % 10 == 0:
        game_state[user_id]['level'] += 1
    
    # Render the grid
    render_game(update, context)

def render_game(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    position = game_state[user_id]['position']
    obstacles = game_state[user_id]['obstacles']
    score = game_state[user_id]['score']
    level = game_state[user_id]['level']
    power_up = game_state[user_id]['power_up']
    
    # Render the grid
    grid = [["[ ]"] * 3 for _ in range(3)]
    grid[2][position - 1] = "[🚶]"
    for i, obstacle in enumerate(obstacles):
        if obstacle == 'P':
            grid[1][i % 3] = "[⭐]"
        else:
            grid[1][obstacle - 1] = "[🚧]"
    
    grid_str = "\n".join("".join(row) for row in grid)
    power_up_status = "Active" if power_up else "Inactive"
    game_info = f"Score: {score}  Level: {level}  Power-Up: {power_up_status}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{grid_str}\n{game_info}")

def update_leaderboard(user_id):
    if user_id in game_state:
        score = game_state[user_id]['score']
        if user_id in leaderboard:
            if score > leaderboard[user_id]:
                leaderboard[user_id] = score
        else:
            leaderboard[user_id] = score

def show_leaderboard(update: Update, context: CallbackContext) -> None:
    if not leaderboard:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No scores yet.")
        return
    leaderboard_str = "\n".join(f"User {user_id}: {score}" for user_id, score in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True))
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Leaderboard:\n{leaderboard_str}")

def main() -> None:
    application = Application.builder().token("7393819055:AAEkqOXGsEbErkP6386MNpB_jH6BSewYi6w").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("left", move_left))
    application.add_handler(CommandHandler("right", move_right))
    application.add_handler(CommandHandler("jump", jump))
    application.add_handler(CommandHandler("leaderboard", show_leaderboard))

    application.run_polling()

if __name__ == '__main__':
    main()
