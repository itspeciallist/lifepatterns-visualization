import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from math import gcd, pi

# ==== Calculate Alive Seconds ====

def calculate_alive_seconds(birthdate_str):
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
        now = datetime.now()
        return int((now - birthdate).total_seconds())
    except Exception as e:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        exit()

# ==== Safe Save Plot ====

def save_plot(filename):
    if not filename.endswith('.png'):
        filename = filename.replace('.jpg', '') + '.png'
    try:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Saved: {filename}")
    except Exception as e:
        print(f"❌ Error saving {filename}: {e}")
    finally:
        plt.close()

# ==== 1. Phyllotaxis Spiral ====

def plot_phyllotaxis(n_points, c=2):
    golden_angle = np.radians(137.5)
    i = np.arange(n_points)
    r = c * np.sqrt(i)
    theta = i * golden_angle
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    plt.figure(figsize=(8,8))
    plt.scatter(x, y, s=0.5, color='green')
    plt.axis('equal'); plt.axis('off')
    plt.title('Phyllotaxis Pattern')
    save_plot('phyllotaxis.png')

# ==== 2. Rose Curve ====

def plot_rose_curve(k, points=1000):
    theta = np.linspace(0, 2 * np.pi, points)
    r = np.sin(k * theta)

    plt.figure(figsize=(6,6))
    plt.polar(theta, r, color='magenta')
    plt.title(f'Rose Curve (k={k})')
    save_plot('rose_curve.png')

# ==== 3. Lissajous Curve ====

def plot_lissajous(a, b, delta=np.pi/2, points=1000):
    t = np.linspace(0, 2 * np.pi, points)
    x = np.sin(a * t + delta)
    y = np.sin(b * t)

    plt.figure(figsize=(6,6))
    plt.plot(x, y, color='blue')
    plt.axis('equal'); plt.axis('off')
    plt.title(f'Lissajous Curve (a={a}, b={b})')
    save_plot('lissajous_curve.png')

# ==== 4. Spirograph ====

def plot_spirograph(R, r, d, points=2000):
    t = np.linspace(0, 2 * np.pi * r / gcd(R, r), points)
    x = (R - r) * np.cos(t) + d * np.cos((R - r) / r * t)
    y = (R - r) * np.sin(t) - d * np.sin((R - r) / r * t)

    plt.figure(figsize=(6,6))
    plt.plot(x, y, color='darkred')
    plt.axis('equal'); plt.axis('off')
    plt.title('Spirograph')
    save_plot('spirograph.png')

# ==== 5. Ulam Spiral (Fixed) ====

def is_prime(num):
    if num < 2: return False
    if num == 2: return True
    if num % 2 == 0: return False
    for i in range(3, int(num**0.5)+1, 2):
        if num % i == 0: return False
    return True

def plot_ulam_spiral(n):
    side = int(np.ceil(np.sqrt(n)))
    grid = np.zeros((side, side), dtype=bool)
    x = y = side // 2
    dx, dy = 0, -1

    for i in range(1, n+1):
        if 0 <= x < side and 0 <= y < side:  # Ensure we're within bounds
            if is_prime(i):
                grid[y, x] = True

        # Determine when to change direction in the spiral
        if (x == y) or (x < y and x + y == side - 1) or (x > y and x + y == side):
            dx, dy = -dy, dx
        x += dx
        y += dy

    plt.figure(figsize=(6,6))
    plt.imshow(grid, cmap='binary')
    plt.title('Ulam Spiral')
    plt.axis('off')
    save_plot('ulam_spiral.png')

# ==== Run All Visuals ====

def main():
    birthdate_str = input("📅 Enter your birthdate (YYYY-MM-DD): ")
    alive_secs = calculate_alive_seconds(birthdate_str)
    print(f"⏱️ Alive seconds: {alive_secs:,}")

    # Derive parameters from alive seconds
    phyllo_points = max(300, alive_secs // 100)
    rose_k = alive_secs % 10 + 2
    lis_a = alive_secs % 9 + 2
    lis_b = alive_secs % 7 + 3
    R = (alive_secs % 9 + 3) * 2
    r = (alive_secs % 5 + 1)
    d = (alive_secs % 10) + 2
    ulam_limit = min(alive_secs // 200, 5000)  # cap to 5000 max

    # Generate all visuals
    plot_phyllotaxis(phyllo_points)
    plot_rose_curve(rose_k)
    plot_lissajous(lis_a, lis_b)
    plot_spirograph(R, r, d)
    plot_ulam_spiral(ulam_limit)

    print("\n🎉 All personalized pattern images saved as PNGs!")

if __name__ == "__main__":
    main()
