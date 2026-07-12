#!/data/data/com.termux/files/usr/bin/bash
# 
#  OFFICIAL_cyber_satyam27 — Ultimate Hosting Tool v3.0      
#     Created By 𒉭 ᎠᴀʀᴋㅤᏙᴇɴᴏᴍㅤ×͜× | 𝐓𝐇𝐄 𝐀𝐋𝐏𝐇𝐀 𒉭 & OFFICIAL_cyber_satyam27            

# 🎨 Colors

R='\033[1;31m'
G='\033[1;32m'
Y='\033[1;33m'
B='\033[1;34m'
P='\033[1;35m'
C='\033[1;36m'
W='\033[1;37m'
D='\033[2m'
RS='\033[0m'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📁 Config
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOME_DIR="/data/data/com.termux/files/home/.termux"
LOG="${HOME_DIR}/.zerodark_log.txt"
URL_FILE="${HOME_DIR}/.zerodark_url.txt"
HISTORY="${HOME_DIR}/.zerodark_history.txt"
CONFIG="${HOME_DIR}/.zerodark_config"
VERSION="3.0"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 Init
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
rm -f "$LOG" "$URL_FILE" 2>/dev/null
declare -a ALL_PIDS=()
START_TIME=$(date +%s)
SELECTED_PATH=""
SELECTED_PORT=""
LOCALHOST_ALREADY_RUNNING=false
LOCALHOST_DETECTED_PORT=""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧹 Cleanup
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cleanup() {
    echo ""
    echo -e "${Y}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RS}"
    echo -e "${Y}  🧹 Stopping all services...${RS}"
    echo -e "${Y}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RS}"

    for pid in "${ALL_PIDS[@]}"; do
        kill "$pid" 2>/dev/null
    done

    pkill -f "php -S 127.0.0.1"   2>/dev/null
    pkill -f "python3 -m http"     2>/dev/null
    pkill -f "cloudflared tunnel"  2>/dev/null
    pkill -f "serveo.net"          2>/dev/null
    pkill -f "localhost.run"       2>/dev/null
    pkill -f "tmole"               2>/dev/null

    local END_TIME UP H M S
    END_TIME=$(date +%s)
    UP=$(( END_TIME - START_TIME ))
    H=$(( UP / 3600 )); M=$(( (UP % 3600) / 60 )); S=$(( UP % 60 ))

    rm -f "$LOG" "$URL_FILE" 2>/dev/null

    echo ""
    echo -e "${G}  ✅ All stopped | Uptime: ${Y}${H}h ${M}m ${S}s${RS}"
    echo -e "${P}  👋 Goodbye Boss! — https://youtube.com/@OFFICIAL_cyber_satyam27${RS}"
    echo ""
    exit 0
}

trap 'cleanup' INT TERM

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🖼️ Banner
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
banner() {
    clear
    echo ""
    echo -e "${Y}  ════════════════════════════════════════════════════${RS}"
  echo -e "${P}██╗  ██╗ ██████╗ ███████╗████████╗██╗  ██╗██╗████████╗${RS}"
echo -e "${W}██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██║ ██╔╝██║╚══██╔══╝${RS}"
echo -e "${B}███████║██║   ██║███████╗   ██║   █████╔╝ ██║   ██║   ${RS}"
echo -e "${R}██╔══██║██║   ██║╚════██║   ██║   ██╔═██╗ ██║   ██║   ${RS}"
echo -e "${Y}██║  ██║╚██████╔╝███████║   ██║   ██║  ██╗██║   ██║   ${RS}"
echo -e "${C}╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝   ╚═╝   ${RS}"

echo -e "${P} ${RS}"
echo -e "${Y}     SRY-𒉭 ᎠᴀʀᴋㅤᏙᴇɴᴏᴍㅤ×͜× | 𝐓𝐇𝐄 𝐀𝐋𝐏𝐇𝐀 𒉭 HOSTKIT${RS}"  ════════════════════════════════════════════════════${RS}"
    echo -e "${G}            🔥 Ultimate Hosting Tool v${VERSION}               ${RS}"
    echo -e "${C}       ⚡ Created by OFFICIAL_cyber_satyam27 & (SRY) ⚡              ${RS}"
    echo -e "${D}${W}        📅 $(date '+%A, %d %B %Y  |  ⏰ %H:%M:%S')   ${RS}"
    echo -e "${Y}  ════════════════════════════════════════════════════${RS}"
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📦 Install Package Helper
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
install_pkg() {
    local pkg_name="$1" cmd_name="$2" desc="$3"

    echo -e "${Y}  🔍 Checking ${C}${pkg_name}${Y} (${desc})...${RS}"

    if command -v "$cmd_name" >/dev/null 2>&1; then
        echo -e "${G}  ✅ Already installed: ${W}${pkg_name}${RS}"
    else
        echo -e "${B}  📥 Installing: ${W}${pkg_name}${RS}"
        if pkg install -y "$pkg_name" >/dev/null 2>&1 && command -v "$cmd_name" >/dev/null 2>&1; then
            echo -e "${G}  ✅ Installed: ${W}${pkg_name}${RS}"
        else
            echo -e "${R}  ❌ Failed: ${W}${pkg_name}${RS}"
        fi
    fi
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📦 Auto Setup
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
auto_setup() {
    banner
    echo -e "${C}  ╔══════════════════════════════════════════╗${RS}"
    echo -e "${C}  ║      📦 AUTO INSTALL REQUIREMENTS       ║${RS}"
    echo -e "${C}  ╚══════════════════════════════════════════╝${RS}"
    echo ""

    echo -e "${Y}  🔄 Updating packages...${RS}"
    pkg update -y  >/dev/null 2>&1
    pkg upgrade -y >/dev/null 2>&1
    echo -e "${G}  ✅ Update done${RS}"
    echo ""

    install_pkg "php"       "php"      "PHP Server"
    install_pkg "python"    "python3"  "Python HTTP Server"
    install_pkg "nodejs"    "node"     "NodeJS Runtime"
    install_pkg "openssh"   "ssh"      "SSH Client"
    install_pkg "curl"      "curl"     "HTTP Client"
    install_pkg "wget"      "wget"     "File Downloader"

    # Cloudflared
    echo -e "${Y}  🔍 Checking ${C}cloudflared${Y}...${RS}"
    if command -v cloudflared >/dev/null 2>&1; then
        echo -e "${G}  ✅ Already installed: cloudflared${RS}"
    else
        echo -e "${B}  📥 Downloading Cloudflared...${RS}"
        local ARCH CF_URL CF_BIN
        ARCH=$(uname -m)
        CF_BIN="$PREFIX/bin/cloudflared"
        case "$ARCH" in
            aarch64|arm64) CF_URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64" ;;
            armv7*)        CF_URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm" ;;
            x86_64)        CF_URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64" ;;
            *)             CF_URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64" ;;
        esac
        if wget -q "$CF_URL" -O "$CF_BIN" 2>/dev/null && chmod +x "$CF_BIN"; then
            echo -e "${G}  ✅ Cloudflared installed (${ARCH})${RS}"
        else
            echo -e "${R}  ❌ Cloudflared download failed${RS}"
        fi
    fi
    echo ""

    # Tunnelmole
    echo -e "${Y}  🔍 Checking ${C}Tunnelmole${Y}...${RS}"
    if command -v tmole >/dev/null 2>&1; then
        echo -e "${G}  ✅ Already installed: Tunnelmole${RS}"
    else
        echo -e "${B}  📥 Installing Tunnelmole via npm...${RS}"
        if npm install -g tunnelmole >/dev/null 2>&1; then
            echo -e "${G}  ✅ Tunnelmole installed${RS}"
        else
            echo -e "${R}  ❌ Tunnelmole failed${RS}"
        fi
    fi
    echo ""

    echo -e "${G}  🎉 Setup complete!${RS}"
    echo ""
    echo -ne "${C}  Press Enter to continue...${RS}"
    read -r
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔍 Detect Running Localhost
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
detect_localhost() {
    LOCALHOST_ALREADY_RUNNING=false
    LOCALHOST_DETECTED_PORT=""

    local running_ports=()
    local running_info=()

    # Check PHP servers
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        local port pid
        port=$(echo "$line" | grep -oE '127\.0\.0\.1:[0-9]+' | grep -oE '[0-9]+$')
        pid=$(echo "$line" | awk '{print $1}')
        if [[ -n "$port" ]]; then
            running_ports+=("$port")
            running_info+=("PHP (PID:${pid}) → port ${port}")
        fi
    done < <(ps aux 2>/dev/null | grep '[p]hp -S 127.0.0.1' || \
             ps -ef 2>/dev/null | grep '[p]hp -S 127.0.0.1' || true)

    # Check Python servers
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        local port pid
        port=$(echo "$line" | grep -oE 'http\.server [0-9]+' | grep -oE '[0-9]+$')
        pid=$(echo "$line" | awk '{print $1}')
        if [[ -n "$port" ]]; then
            running_ports+=("$port")
            running_info+=("Python (PID:${pid}) → port ${port}")
        fi
    done < <(ps aux 2>/dev/null | grep '[p]ython3 -m http.server' || \
             ps -ef 2>/dev/null | grep '[p]ython3 -m http.server' || true)

    # Fallback: check common ports directly
    if [[ ${#running_ports[@]} -eq 0 ]]; then
        for test_port in 8080 8888 3000 5000 8000 4000 9000; do
            if (echo >/dev/tcp/127.0.0.1/${test_port}) 2>/dev/null; then
                running_ports+=("$test_port")
                running_info+=("Unknown server → port ${test_port}")
            fi
        done
    fi

    if [[ ${#running_ports[@]} -gt 0 ]]; then
        LOCALHOST_ALREADY_RUNNING=true
        LOCALHOST_DETECTED_PORT="${running_ports[0]}"

        echo ""
        echo -e "${G}  ╔══════════════════════════════════════════════════════╗${RS}"
        echo -e "${G}  ║     🟢 RUNNING LOCALHOST DETECTED!                  ║${RS}"
        echo -e "${G}  ╠══════════════════════════════════════════════════════╣${RS}"

        local idx=1
        for info in "${running_info[@]}"; do
            echo -e "${Y}  ║  [${idx}] ${W}${info}${RS}"
            (( idx++ ))
        done

        echo -e "${G}  ╚══════════════════════════════════════════════════════╝${RS}"
        echo ""

        return 0
    else
        LOCALHOST_ALREADY_RUNNING=false
        return 1
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔌 Get Port (Default Y / Custom N)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
get_port() {
    echo ""
    echo -e "${Y}  ┌──────────────────────────────────────────┐${RS}"
    echo -e "${Y}  │          🔌 PORT SELECTION               │${RS}"
    echo -e "${Y}  └──────────────────────────────────────────┘${RS}"
    echo ""
    echo -e "${W}  Default port is ${G}8080${RS}"
    echo ""
    echo -ne "${C}  Use default port 8080? [${G}Y${C}/${R}n${C}]: ${RS}"
    read -r port_choice

    case "${port_choice,,}" in
        ""|"y"|"yes")
            SELECTED_PORT="8080"
            echo -e "${G}  ✅ Using default port: ${Y}8080${RS}"
            ;;
        "n"|"no")
            echo ""
            echo -e "${C}  Enter custom port number (1025–65534):${RS}"
            echo -ne "${G}  👉 Port: ${RS}"
            read -r custom_port

            if [[ "$custom_port" =~ ^[0-9]+$ ]] \
            && (( custom_port > 1024 && custom_port < 65535 )); then
                SELECTED_PORT="$custom_port"
                echo -e "${G}  ✅ Using custom port: ${Y}${custom_port}${RS}"
            else
                SELECTED_PORT="8080"
                echo -e "${Y}  ⚠️  Invalid port! Using default: ${Y}8080${RS}"
            fi
            ;;
        *)
            SELECTED_PORT="8080"
            echo -e "${Y}  ⚠️  Invalid input. Using default: ${Y}8080${RS}"
            ;;
    esac
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔌 Get Port for Forwarding Only
#    (when localhost already running)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
get_forward_port() {
    local detected="$1"

    echo ""
    echo -e "${Y}  ┌──────────────────────────────────────────┐${RS}"
    echo -e "${Y}  │     🔌 WHICH PORT TO FORWARD?            │${RS}"
    echo -e "${Y}  └──────────────────────────────────────────┘${RS}"
    echo ""
    echo -e "${W}  Detected running port: ${G}${detected}${RS}"
    echo ""
    echo -ne "${C}  Use detected port ${G}${detected}${C}? [${G}Y${C}/${R}n${C}]: ${RS}"
    read -r fwd_choice

    case "${fwd_choice,,}" in
        ""|"y"|"yes")
            SELECTED_PORT="$detected"
            echo -e "${G}  ✅ Forwarding port: ${Y}${detected}${RS}"
            ;;
        "n"|"no")
            echo ""
            echo -ne "${C}  Enter port to forward: ${RS}"
            read -r manual_port
            if [[ "$manual_port" =~ ^[0-9]+$ ]] \
            && (( manual_port > 1024 && manual_port < 65535 )); then
                SELECTED_PORT="$manual_port"
                echo -e "${G}  ✅ Forwarding port: ${Y}${manual_port}${RS}"
            else
                SELECTED_PORT="$detected"
                echo -e "${Y}  ⚠️  Invalid! Using detected: ${Y}${detected}${RS}"
            fi
            ;;
        *)
            SELECTED_PORT="$detected"
            echo -e "${G}  ✅ Forwarding port: ${Y}${detected}${RS}"
            ;;
    esac
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📁 Get Directory Path
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
get_path() {
    echo ""
    echo -e "${Y}  ┌──────────────────────────────────────────┐${RS}"
    echo -e "${Y}  │       📁 SELECT DIRECTORY TO HOST        │${RS}"
    echo -e "${Y}  └──────────────────────────────────────────┘${RS}"
    echo -e "${D}${W}  Examples:${RS}"
    echo -e "${D}${C}    /sdcard/Download/mysite${RS}"
    echo -e "${D}${C}    /storage/emulated/0${RS}"
    echo -e "${W}  💡 Press Enter = current directory${RS}"

    local last_path=""
    if [[ -f "$CONFIG" ]]; then
        last_path=$(grep "^LAST_PATH=" "$CONFIG" 2>/dev/null | cut -d'=' -f2-)
        if [[ -n "$last_path" ]]; then
            echo -e "${D}${W}  Last used: ${Y}${last_path}${RS}"
            echo -e "${D}${W}  Type ${G}L${W} to reuse${RS}"
        fi
    fi
    echo ""
    echo -ne "${G}  👉 Path: ${RS}"
    read -r path_input

    if [[ "${path_input,,}" == "l" ]] && [[ -n "$last_path" ]]; then
        path_input="$last_path"
        echo -e "${G}  ✅ Using last path${RS}"
    fi

    local dir_path=""
    if [[ -z "$path_input" ]]; then
        dir_path="$(pwd)"
    else
        dir_path="${path_input%/}"
        dir_path="${dir_path/#\~/$HOME}"
        dir_path="${dir_path//\/storage\/emulated\/0/\/sdcard}"
    fi

    if [[ ! -d "$dir_path" ]]; then
        echo -e "${Y}  ⚠️  Not found. Creating...${RS}"
        if mkdir -p "$dir_path" 2>/dev/null; then
            echo -e "${G}  ✅ Created${RS}"
        else
            echo -e "${R}  ❌ Cannot create. Using current dir.${RS}"
            dir_path="$(pwd)"
        fi
    fi

    echo "LAST_PATH=${dir_path}" > "$CONFIG"

    local fc
    fc=$(ls "$dir_path" 2>/dev/null | wc -l)
    echo -e "${G}  ✅ Directory: ${Y}${dir_path}${G} (${fc} files)${RS}"
    echo ""

    SELECTED_PATH="$dir_path"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🐘 Start PHP Server
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
start_php() {
    local dir_path="$1"
    local port="$2"

    pkill -f "php -S 127.0.0.1:${port}" 2>/dev/null
    sleep 0.5

    [[ ! -d "$dir_path" ]] && {
        echo -e "${R}  ❌ Directory not found: ${dir_path}${RS}"
        return 1
    }

    echo -e "${C}  🚀 Starting PHP server → port ${Y}${port}${RS}"
    php -S "127.0.0.1:${port}" -t "$dir_path" >/dev/null 2>&1 &
    local php_pid=$!
    sleep 2

    if kill -0 "$php_pid" 2>/dev/null; then
        ALL_PIDS+=("$php_pid")
        echo -e "${G}  ✅ PHP server running [PID: ${php_pid}]${RS}"
        return 0
    else
        echo -e "${R}  ❌ PHP server failed!${RS}"
        return 1
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🌐 Show URL Box
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
show_url_box() {
    local public_url="$1"
    local port="$2"
    local tunnel="$3"

    echo "$public_url" > "$URL_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${tunnel}] ${public_url}" >> "$HISTORY"

    local local_ip
    local_ip=$(hostname -I 2>/dev/null | awk '{print $1}')

    echo ""
    echo ""
echo -e "${G}🎉 SERVER IS LIVE! 🎉${RS}\n"
echo -e "${C}📍 Local: ${Y}http://127.0.0.1:${port}${RS}\n"

[[ -n "$local_ip" ]] && \
echo -e "${Y}   http://${local_ip}:${port} (LAN)${RS}\n"
echo -e "${C}🌍 Public (Share This!):${G}   ${public_url}${RS}\n"
echo -e "${R}⚠️ Press Ctrl+C to stop server${RS}"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⏳ Wait for URL in log
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
wait_for_url() {
    local pattern="$1"
    local max_wait="${2:-30}"
    local found_url=""

    echo -e "${Y}  ⏳ Waiting for public URL...${RS}"
    local i=0
    while (( i < max_wait )); do
        sleep 1
        printf "\r${D}  [%d/%d]...${RS}" "$((i+1))" "$max_wait"
        if [[ -f "$LOG" ]]; then
            found_url=$(grep -oE "$pattern" "$LOG" 2>/dev/null | tail -1)
            [[ -n "$found_url" ]] && break
        fi
        (( i++ ))
    done
    echo ""
    echo "$found_url"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔥 SMART SETUP — Ask: Localhost already running?
#    YES → Only ask port → Forward directly
#    NO  → Ask path + port → Start server + Forward
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
smart_setup_for_tunnel() {
    local tunnel_name="$1"

    echo ""
    echo -e "${C}  ┌──────────────────────────────────────────────────┐${RS}"
    echo -e "${C}  │    🔍 CHECKING FOR RUNNING LOCALHOST SERVER...   │${RS}"
    echo -e "${C}  └──────────────────────────────────────────────────┘${RS}"

    # Auto detect first
    detect_localhost

    if [[ "$LOCALHOST_ALREADY_RUNNING" == true ]]; then
        # ━━━ Localhost IS running ━━━
        echo ""
        echo -e "${G}  ✅ Localhost is already running!${RS}"
        echo ""
        echo -ne "${C}  Use existing localhost for ${Y}${tunnel_name}${C}? [${G}Y${C}/${R}n${C}]: ${RS}"
        read -r use_existing

        case "${use_existing,,}" in
            ""|"y"|"yes")
                # Only ask port
                echo ""
                echo -e "${G}  ✅ Great! Only need the port to forward.${RS}"
                get_forward_port "$LOCALHOST_DETECTED_PORT"
                echo -e "${C}  ⏩ Skipping server start — forwarding directly...${RS}"
                return 0
                ;;
            "n"|"no")
                # Start new server
                echo ""
                echo -e "${Y}  📝 Starting NEW localhost server...${RS}"
                get_path
                get_port
                start_php "$SELECTED_PATH" "$SELECTED_PORT" || return 1
                return 0
                ;;
            *)
                get_forward_port "$LOCALHOST_DETECTED_PORT"
                return 0
                ;;
        esac
    else
        # ━━━ Localhost NOT running ━━━
        echo ""
        echo -e "${Y}  ⚠️  No running localhost detected.${RS}"
        echo ""
        echo -ne "${C}  Is localhost already running somewhere? [${R}y${C}/${G}N${C}]: ${RS}"
        read -r manual_confirm

        case "${manual_confirm,,}" in
            "y"|"yes")
                # User says yes — just ask port
                echo ""
                echo -e "${Y}  Okay! Enter the port your server is running on:${RS}"
                echo -ne "${G}  👉 Port: ${RS}"
                read -r manual_port

                if [[ "$manual_port" =~ ^[0-9]+$ ]] \
                && (( manual_port > 0 && manual_port < 65535 )); then
                    SELECTED_PORT="$manual_port"
                    echo -e "${G}  ✅ Will forward port: ${Y}${manual_port}${RS}"
                else
                    echo -e "${R}  ❌ Invalid port!${RS}"
                    return 1
                fi
                return 0
                ;;
            ""|"n"|"no"|*)
                # Start fresh server
                echo ""
                echo -e "${C}  📝 Let's start a new localhost server.${RS}"
                get_path
                get_port
                start_php "$SELECTED_PATH" "$SELECTED_PORT" || return 1
                return 0
                ;;
        esac
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1️⃣ PHP Local Only
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
php_local() {
    banner
    echo -e "${G}  ╔══════════════════════════════════════════╗${RS}"
    echo -e "${G}  ║        🐘 PHP LOCAL SERVER               ║${RS}"
    echo -e "${G}  ╚══════════════════════════════════════════╝${RS}"

    get_path
    get_port

    start_php "$SELECTED_PATH" "$SELECTED_PORT" || return

    local local_ip
    local_ip=$(hostname -I 2>/dev/null | awk '{print $1}')

    echo ""
    echo -e "${G}  ╔══════════════════════════════════════════════════════╗${RS}"
    echo -e "${G}  ║        🐘 PHP SERVER RUNNING                        ║${RS}"
    echo -e "${G}  ╠══════════════════════════════════════════════════════╣${RS}"
    echo -e "${Y}  ║    http://127.0.0.1:${SELECTED_PORT}${RS}"
    echo -e "${Y}  ║    http://localhost:${SELECTED_PORT}${RS}"
    [[ -n "$local_ip" ]] && \
    echo -e "${Y}  ║    http://${local_ip}:${SELECTED_PORT} (LAN)${RS}"
    echo -e "${G}  ╠══════════════════════════════════════════════════════╣${RS}"
    echo -e "${G}  ║  ⚠️  Press ${R}Ctrl+C${G} to stop                        ║${RS}"
    echo -e "${G}  ╚══════════════════════════════════════════════════════╝${RS}"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2️⃣ Python Local Only
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
python_local() {
    banner
    echo -e "${Y}  ╔══════════════════════════════════════════╗${RS}"
    echo -e "${Y}  ║        🐍 PYTHON LOCAL SERVER            ║${RS}"
    echo -e "${Y}  ╚══════════════════════════════════════════╝${RS}"

    get_path
    get_port

    echo -e "${C}  🚀 Starting Python server → port ${Y}${SELECTED_PORT}${RS}"
    python3 -m http.server "$SELECTED_PORT" --directory "$SELECTED_PATH" >/dev/null 2>&1 &
    local py_pid=$!
    ALL_PIDS+=("$py_pid")
    sleep 2

    if kill -0 "$py_pid" 2>/dev/null; then
        local local_ip
        local_ip=$(hostname -I 2>/dev/null | awk '{print $1}')

        echo ""
        echo -e "${Y}  ╔══════════════════════════════════════════════════════╗${RS}"
        echo -e "${Y}  ║        🐍 PYTHON SERVER RUNNING                     ║${RS}"
        echo -e "${Y}  ╠══════════════════════════════════════════════════════╣${RS}"
        echo -e "${G}  ║    http://127.0.0.1:${SELECTED_PORT}${RS}"
        echo -e "${G}  ║    http://localhost:${SELECTED_PORT}${RS}"
        [[ -n "$local_ip" ]] && \
        echo -e "${G}  ║    http://${local_ip}:${SELECTED_PORT} (LAN)${RS}"
        echo -e "${Y}  ╠══════════════════════════════════════════════════════╣${RS}"
        echo -e "${Y}  ║  ⚠️  Press ${R}Ctrl+C${Y} to stop                        ║${RS}"
        echo -e "${Y}  ╚══════════════════════════════════════════════════════╝${RS}"
    else
        echo -e "${R}  ❌ Python server failed!${RS}"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3️⃣ Cloudflared Tunnel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cloudflared_tunnel() {
    banner
    echo -e "${C}  ╔══════════════════════════════════════════╗${RS}"
    echo -e "${C}  ║       ☁️  CLOUDFLARED TUNNEL              ║${RS}"
    echo -e "${C}  ╚══════════════════════════════════════════╝${RS}"

    if ! command -v cloudflared >/dev/null 2>&1; then
        echo -e "${R}  ❌ Cloudflared not installed! Run option 8.${RS}"
        sleep 3; return 1
    fi

    smart_setup_for_tunnel "Cloudflared" || return 1

    echo ""
    echo -e "${C}  🌐 Launching Cloudflared tunnel on port ${Y}${SELECTED_PORT}${C}...${RS}"
    rm -f "$LOG"

    cloudflared tunnel --url "http://127.0.0.1:${SELECTED_PORT}" \
        --logfile "$LOG" --no-autoupdate >/dev/null 2>&1 &
    ALL_PIDS+=($!)

    local url
    url=$(wait_for_url 'https://[-0-9a-z]+\.trycloudflare\.com' 30)

    if [[ -n "$url" ]]; then
        show_url_box "$url" "$SELECTED_PORT" "Cloudflared"
    else
        echo -e "${R}  ❌ Cloudflared URL not found!${RS}"
        echo -e "${Y}  💡 Check internet / reinstall (option 8)${RS}"
        echo -e "${D}${W}  --- Last 5 log lines ---${RS}"
        tail -5 "$LOG" 2>/dev/null
        sleep 4; return 1
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4️⃣ Serveo Tunnel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
serveo_tunnel() {
    banner
    echo -e "${B}  ╔══════════════════════════════════════════╗${RS}"
    echo -e "${B}  ║        🔗 SERVEO SSH TUNNEL              ║${RS}"
    echo -e "${B}  ╚══════════════════════════════════════════╝${RS}"

    if ! command -v ssh >/dev/null 2>&1; then
        echo -e "${R}  ❌ OpenSSH not installed! Run option 8.${RS}"
        sleep 3; return 1
    fi

    smart_setup_for_tunnel "Serveo" || return 1

    echo ""
    echo -e "${C}  🌐 Connecting to Serveo on port ${Y}${SELECTED_PORT}${C}...${RS}"
    rm -f "$LOG"

    ssh -o StrictHostKeyChecking=no \
        -o ServerAliveInterval=60 \
        -o ServerAliveCountMax=3 \
        -o ConnectTimeout=15 \
        -R "80:localhost:${SELECTED_PORT}" \
        serveo.net > "$LOG" 2>&1 &
    ALL_PIDS+=($!)

    local url
    url=$(wait_for_url 'https?://[a-zA-Z0-9.-]+\.serveo\.net' 25)

    if [[ -n "$url" ]]; then
        show_url_box "$url" "$SELECTED_PORT" "Serveo"
    else
        echo -e "${R}  ❌ Serveo failed!${RS}"
        echo -e "${Y}  💡 Serveo may be down. Try Cloudflared.${RS}"
        sleep 3; return 1
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5️⃣ Localhost.run Tunnel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
localhostrun_tunnel() {
    banner
    echo -e "${P}  ╔══════════════════════════════════════════╗${RS}"
    echo -e "${P}  ║      🏃 LOCALHOST.RUN TUNNEL             ║${RS}"
    echo -e "${P}  ╚══════════════════════════════════════════╝${RS}"

    if ! command -v ssh >/dev/null 2>&1; then
        echo -e "${R}  ❌ OpenSSH not installed! Run option 8.${RS}"
        sleep 3; return 1
    fi

    smart_setup_for_tunnel "Localhost.run" || return 1

    echo ""
    echo -e "${C}  🌐 Connecting to Localhost.run on port ${Y}${SELECTED_PORT}${C}...${RS}"
    rm -f "$LOG"

    ssh -o StrictHostKeyChecking=no \
        -o ServerAliveInterval=60 \
        -o ConnectTimeout=15 \
        -R "80:localhost:${SELECTED_PORT}" \
        nokey@localhost.run > "$LOG" 2>&1 &
    ALL_PIDS+=($!)

    # Try multiple URL patterns
    local url="" i=0
    echo -e "${Y}  ⏳ Waiting for public URL...${RS}"
    while (( i < 25 )); do
        sleep 1
        printf "\r${D}  [%d/25]...${RS}" "$((i+1))"
        if [[ -f "$LOG" ]]; then
            url=$(grep -oE 'https://[a-zA-Z0-9_-]+\.lhr\.life' "$LOG" 2>/dev/null | head -1)

            [[ -z "$url" ]] && \
            url=$(grep -oE 'https?://[a-zA-Z0-9._-]+\.(lhr\.life)' "$LOG" 2>/dev/null | head -1)
            [[ -n "$url" ]] && break
        fi
        (( i++ ))
    done
    echo ""

    if [[ -n "$url" ]]; then
        show_url_box "$url" "$SELECTED_PORT" "Localhost.run"
    else
        echo -e "${R}  ❌ Localhost.run failed!${RS}"
        echo -e "${Y}  💡 Try Cloudflared instead.${RS}"
        tail -5 "$LOG" 2>/dev/null
        sleep 3; return 1
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6️⃣ Tunnelmole Tunnel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tunnelmole_tunnel() {
    banner
    echo -e "${Y}  ╔══════════════════════════════════════════╗${RS}"
    echo -e "${Y}  ║         🕳️  TUNNELMOLE TUNNEL             ║${RS}"
    echo -e "${Y}  ╚══════════════════════════════════════════╝${RS}"

    if ! command -v tmole >/dev/null 2>&1; then
        echo -e "${R}  ❌ Tunnelmole not installed! Run option 8.${RS}"
        sleep 3; return 1
    fi

    smart_setup_for_tunnel "Tunnelmole" || return 1

    echo ""
    echo -e "${C}  🌐 Starting Tunnelmole on port ${Y}${SELECTED_PORT}${C}...${RS}"
    rm -f "$LOG"

    tmole "$SELECTED_PORT" > "$LOG" 2>&1 &
    ALL_PIDS+=($!)

    local url
    url=$(wait_for_url 'https://[a-zA-Z0-9.-]+\.tunnelmole\.(net|com)' 30)

    if [[ -n "$url" ]]; then
        show_url_box "$url" "$SELECTED_PORT" "Tunnelmole"
    else
        echo -e "${R}  ❌ Tunnelmole failed!${RS}"
        echo -e "${Y}  💡 Reinstall (option 8)${RS}"
        tail -5 "$LOG" 2>/dev/null
        sleep 3; return 1
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7️⃣ All Tunnels At Once
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
all_tunnels() {
    banner
    echo -e "${R}  ╔══════════════════════════════════════════╗${RS}"
    echo -e "${R}  ║    🚀 ALL TUNNELS SIMULTANEOUSLY         ║${RS}"
    echo -e "${R}  ╚══════════════════════════════════════════╝${RS}"

    smart_setup_for_tunnel "ALL Tunnels" || return 1

    local port="$SELECTED_PORT"
    local cf_log="/tmp/zd_cf_$$.log"
    local sv_log="/tmp/zd_sv_$$.log"
    local lr_log="/tmp/zd_lr_$$.log"

    echo ""
    echo -e "${Y}  🚀 Launching all tunnels on port ${G}${port}${Y}...${RS}"

    if command -v cloudflared >/dev/null 2>&1; then
        echo -e "${C}  ☁️  Cloudflared starting...${RS}"
        cloudflared tunnel --url "http://127.0.0.1:${port}" \
            --logfile "$cf_log" --no-autoupdate >/dev/null 2>&1 &
        ALL_PIDS+=($!)
    fi

    if command -v ssh >/dev/null 2>&1; then
        echo -e "${B}  🔗 Serveo starting...${RS}"
        ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 \
            -R "80:localhost:${port}" serveo.net > "$sv_log" 2>&1 &
        ALL_PIDS+=($!)

        echo -e "${P}  🏃 Localhost.run starting...${RS}"
        ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 \
            -R "80:localhost:${port}" nokey@localhost.run > "$lr_log" 2>&1 &
        ALL_PIDS+=($!)
    fi

    echo ""
    echo -e "${Y}  ⏳ Collecting URLs (30s)...${RS}"
    sleep 28

    local cf_url sv_url lr_url
    cf_url=$(grep -oE 'https://[-0-9a-z]+\.trycloudflare\.com' "$cf_log" 2>/dev/null | tail -1)
    sv_url=$(grep -oE 'https?://[a-zA-Z0-9.-]+\.serveo\.net' "$sv_log" 2>/dev/null | head -1)
    lr_url=$(grep -oE 'https://[a-zA-Z0-9_-]+\.lhr\.life' "$lr_log" 2>/dev/null | head -1)

    rm -f "$cf_log" "$sv_log" "$lr_log"

    echo ""
    echo -e "${G}  ╔══════════════════════════════════════════════════════╗${RS}"
    echo -e "${G}  ║          🌐 ALL PUBLIC URLS                         ║${RS}"
    echo -e "${G}  ╠══════════════════════════════════════════════════════╣${RS}"
    echo -e "${C}  ║  📍 Local: http://127.0.0.1:${port}${RS}"
    echo -e "${G}  ╠══════════════════════════════════════════════════════╣${RS}"

    local any=false
    if [[ -n "$cf_url" ]]; then
        echo -e "${G}  ║  ☁️  ${cf_url}${RS}"
        echo "$cf_url" > "$URL_FILE"
        any=true
    else
        echo -e "${R}  ║  ☁️  Cloudflared: ❌ Failed${RS}"
    fi

    if [[ -n "$sv_url" ]]; then
        echo -e "${G}  ║  🔗 ${sv_url}${RS}"
        any=true
    else
        echo -e "${R}  ║  🔗 Serveo: ❌ Failed${RS}"
    fi

    if [[ -n "$lr_url" ]]; then
        echo -e "${G}  ║  🏃 ${lr_url}${RS}"
        any=true
    else
        echo -e "${R}  ║  🏃 Localhost.run: ❌ Failed${RS}"
    fi

    echo -e "${G}  ╠══════════════════════════════════════════════════════╣${RS}"
    echo -e "${G}  ║  ⚠️  Press ${R}Ctrl+C${G} to stop ALL                     ║${RS}"
    echo -e "${G}  ╚══════════════════════════════════════════════════════╝${RS}"

    [[ "$any" == false ]] && {
        echo -e "${R}  ❌ All failed! Check internet.${RS}"
        sleep 4; return 1
    }
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📜 URL History
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
view_history() {
    banner
    echo -e "${C}  ╔══════════════════════════════════════════╗${RS}"
    echo -e "${C}  ║           📜 URL HISTORY                ║${RS}"
    echo -e "${C}  ╚══════════════════════════════════════════╝${RS}"
    echo ""

    if [[ ! -f "$HISTORY" ]] || [[ ! -s "$HISTORY" ]]; then
        echo -e "${Y}  No history yet.${RS}"
    else
        echo -e "${W}  Last 20 entries:${RS}"
        echo ""
        tail -20 "$HISTORY" | while IFS= read -r line; do
            echo -e "${G}  ➤ ${Y}${line}${RS}"
        done
    fi

    echo ""
    echo -ne "${C}  Press Enter to go back...${RS}"
    read -r
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎮 Main Menu
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
menu() {
    while true; do
        # Kill previous
        for pid in "${ALL_PIDS[@]}"; do
            kill "$pid" 2>/dev/null
        done
        ALL_PIDS=()
        START_TIME=$(date +%s)

        banner

        echo -e "${C}  ╔══════════════════════════════════════════════╗${RS}"
        echo -e "${C}  ║           SELECT HOSTING OPTION              ║${RS}"
        echo -e "${C}  ╠══════════════════════════════════════════════╣${RS}"
        echo -e "${C}  ║  ${Y}🏠 LOCAL SERVERS                            ${C}║${RS}"
        echo -e "${C}  ║  ${G}[1]${W} 🐘 PHP Local Server                     ${C}║${RS}"
        echo -e "${C}  ║  ${G}[2]${W} 🐍 Python Local Server                  ${C}║${RS}"
        echo -e "${C}  ╠══════════════════════════════════════════════╣${RS}"
        echo -e "${C}  ║  ${Y}🌐 PUBLIC TUNNELS (Auto-Detect Localhost)   ${C}║${RS}"
        echo -e "${C}  ║  ${G}[3]${W} ☁️  Cloudflared  ${D}(Best)${RS}                 ${C} ║${RS}"
        echo -e "${C}  ║  ${G}[4]${W} 🔗 Serveo Tunnel                        ${C}║${RS}"
        echo -e "${C}  ║  ${G}[5]${W} 🏃 Localhost.run                        ${C}║${RS}"
        echo -e "${C}  ║  ${G}[6]${W} 🕳️  Tunnelmole                           ${C}║${RS}"
        echo -e "${C}  ║  ${R}[7]${W} 🚀 ALL Tunnels At Once                  ${C}║${RS}"
        echo -e "${C}  ╠══════════════════════════════════════════════╣${RS}"
        echo -e "${C}  ║  ${Y}🛠️  TOOLS                                    ${C}║${RS}"
        echo -e "${C}  ║  ${G}[8]${W} 📦 Install/Update Packages              ${C}║${RS}"
        echo -e "${C}  ║  ${G}[9]${W} 📜 View URL History                     ${C}║${RS}"
        echo -e "${C}  ║  ${R}[0]${W} ❌ Exit                                 ${C}║${RS}"
        echo -e "${C}  ╚══════════════════════════════════════════════╝${RS}"
        echo ""
        echo -ne "${G}  👉 Choose [0-9]: ${RS}"
        read -r choice

        case "$choice" in
            1) php_local          ;;
            2) python_local       ;;
            3) cloudflared_tunnel ;;
            4) serveo_tunnel      ;;
            5) localhostrun_tunnel;;
            6) tunnelmole_tunnel  ;;
            7) all_tunnels        ;;
            8) auto_setup         ;;
            9) view_history       ;;
            0)
                echo ""
                echo -ne "${Y}  Exit? [${G}Y${Y}/${R}n${Y}]: ${RS}"
                read -r cf
                [[ "${cf,,}" != "n" ]] && cleanup
                ;;
            *)
                echo -e "${R}  ❌ Invalid! Choose 0–9${RS}"
                sleep 1
                continue
                ;;
        esac

        # Keep server alive
        if [[ "$choice" =~ ^[1-7]$ ]]; then
            echo ""
            echo -e "${G}  🟢 Server running — Press ${R}Ctrl+C${G} to stop${RS}"
            while true; do
                sleep 5
                local up h m s
                up=$(( $(date +%s) - START_TIME ))
                h=$(( up/3600 )); m=$(( (up%3600)/60 )); s=$(( up%60 ))
                printf "\r${D}${W}  ⏱ Uptime: %02dh %02dm %02ds${RS}" "$h" "$m" "$s"
            done
        fi
    done
}

menu
