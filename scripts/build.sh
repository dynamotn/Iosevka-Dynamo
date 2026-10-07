#!/usr/bin/env bash
# @file build.sh
# @brief Build Iosevka Dynamo fonts
# @description Build Iosevka Dynamo fonts, Nerd Font patched fonts and web fonts
SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
# shellcheck source=lib/dybatpho/init.sh
. "$SCRIPT_DIR/lib/dybatpho/init.sh"
dybatpho::register_err_handler

FONT_FAMILY_NAME="Iosevka Dynamo"
FONT_FAMILY_VERSION="v2.1.0"
FIRACODE_VERSION="3.1"
IOSEVKA_VERSION="latest"
IOSEVKA_VARIANT="FixedSS05" # Use fixed version of Fira Mono style variant
# Public URL of the site hosted on GitHub Pages
WEB_BASE_URL="${WEB_BASE_URL:-https://dynamotn.github.io/Iosevka-Dynamo}"

ASSETS_DIR=$(realpath "$SCRIPT_DIR/../assets")
OUTPUT_DIR=$(realpath "$SCRIPT_DIR/../build")
WEB_DIR="$(realpath "$SCRIPT_DIR/..")/public"
SRC_DIR=$(realpath "$SCRIPT_DIR/../src")
TEST_DIR=$(realpath "$SCRIPT_DIR/../test")

#######################################
# @description Check required tools to build fonts
# @noargs
#######################################
function _prerequisite {
  dybatpho::require 'grep'
  dybatpho::require 'unzip'
  dybatpho::require 'fontforge'
  dybatpho::require 'docker'
}

#######################################
# @description Download Iosevka font from GitHub release
# @noargs
#######################################
function _download_iosevka {
  if dybatpho::is file "$ASSETS_DIR/IosevkaFixedSS05-Regular.ttf"; then
    dybatpho::info "Already have Iosevka font"
    return
  fi
  if [ "${IOSEVKA_VERSION}" == "latest" ]; then
    local release_file
    dybatpho::create_temp release_file ".json"
    dybatpho::curl_do https://api.github.com/repos/be5invis/Iosevka/releases/latest "$release_file"
    IOSEVKA_VERSION=$(grep -Po "tag_name\": \"(\K.*)(?=\",)" "$release_file")
  fi
  dybatpho::notice "Downloading Iosevka font version: ${IOSEVKA_VERSION}"
  local zip_file
  dybatpho::create_temp zip_file ".zip"
  local release_url="https://github.com/be5invis/Iosevka/releases/download/${IOSEVKA_VERSION}"
  dybatpho::curl_download \
    "${release_url}/PkgTTF-Iosevka${IOSEVKA_VARIANT}-${IOSEVKA_VERSION:1}.zip" \
    "$zip_file"
  unzip -qqo "$zip_file" -d "${ASSETS_DIR}"
  dybatpho::success "Downloaded Iosevka"
}

#######################################
# @description Download FiraCode font from GitHub repository
# @noargs
#######################################
function _download_firacode {
  dybatpho::notice "Downloading FiraCode font version: ${FIRACODE_VERSION}"
  local -a fira_style_names=("Regular" "Bold")
  for style in "${fira_style_names[@]}"; do
    if dybatpho::is file "${ASSETS_DIR}/FiraCode-${style}.otf"; then
      dybatpho::info "Already have FiraCode ${style}"
      continue
    fi
    dybatpho::curl_download \
      "https://raw.githubusercontent.com/tonsky/FiraCode/${FIRACODE_VERSION}/distr/otf/FiraCode-${style}.otf" \
      "${ASSETS_DIR}/FiraCode-${style}.otf"
  done
  dybatpho::success "Downloaded FiraCode"
}

#######################################
# @description Patch built fonts with Nerd Font glyphs by its docker image
# @noargs
#######################################
function _patch_nerd {
  dybatpho::notice "Patching Nerd Font"
  local -a style_names=("Regular" "Italic" "Bold" "BoldItalic")
  local -a font_suffixes=("" " Italic" " Bold" " Bold Italic")
  local style_count=0
  for style_name in "${style_names[@]}"; do
    local lower_style_name
    lower_style_name=$(dybatpho::lower "$style_name")
    local input_filename="iosevka-dynamo-${lower_style_name}.ttf"
    local patched_filename="IosevkaDynamoNerd-${style_name}.ttf"
    local output_filename="iosevka-dynamo-nerd-${lower_style_name}.ttf"
    docker run --rm \
      -v "$OUTPUT_DIR/${input_filename}":/in/iosevka-dynamo.ttf \
      -v "$OUTPUT_DIR":/out \
      nerdfonts/patcher \
      --name "'Iosevka Dynamo Nerd${font_suffixes[$style_count]}'" \
      --mono --fontawesome --codicons --material --octicons --careful
    ((style_count += 1))
    # dyshellint disable=BSG035 Docker writes patched font as root
    sudo mv "${OUTPUT_DIR}/${patched_filename}" \
      "${OUTPUT_DIR}/${output_filename}"
    # dyshellint disable=BSG035 Docker writes patched font as root
    sudo chown "$USER" "${OUTPUT_DIR}/${output_filename}"
  done
}

#######################################
# @description Generate WOFF2 fonts, stylesheets and demo page for web
# @noargs
#######################################
function _generate_web {
  dybatpho::notice "Generating web fonts to ${WEB_DIR}"
  mkdir -p "$WEB_DIR"
  "${SRC_DIR}/web.py" \
    "$OUTPUT_DIR" \
    "$WEB_DIR" \
    -v "$FONT_FAMILY_VERSION" \
    -u "$WEB_BASE_URL" \
    -s "${TEST_DIR}/pattern.txt"
}

#######################################
# @description Entrypoint of script
# @arg $@ string Arguments of script, unused
#######################################
function _main {
  _prerequisite
  _download_iosevka
  _download_firacode

  local -a style_names=("Regular" "Italic" "Oblique" "Bold" "BoldItalic" "BoldOblique")
  for style_name in "${style_names[@]}"; do
    local fira_style="Regular"
    [[ "$style_name" =~ Bold* ]] && fira_style="Bold"
    dybatpho::notice "Make font ${FONT_FAMILY_NAME} ${style_name}"
    "${SRC_DIR}/main.py" \
      "${ASSETS_DIR}/Iosevka${IOSEVKA_VARIANT}-${style_name}.ttf" \
      "$(realpath "${ASSETS_DIR}/FiraCode-${fira_style}.otf")" \
      -n "$FONT_FAMILY_NAME" \
      -s "$style_name" -d \
      -v "${FONT_FAMILY_VERSION}" \
      -D "$OUTPUT_DIR"
  done
  dybatpho::success "Created font $FONT_FAMILY_NAME"

  _patch_nerd
  dybatpho::success "Patched Nerd Font"

  _generate_web
  dybatpho::success "Generated web fonts"
}

_main "$@"
