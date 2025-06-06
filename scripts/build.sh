#!/usr/bin/env bash
SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
# shellcheck source=lib/dybatpho/init.sh
. "$SCRIPT_DIR/lib/dybatpho/init.sh"
dybatpho::register_err_handler

FONT_FAMILY_NAME="Iosevka Dynamo"
FONT_FAMILY_VERSION="v2.1.0"
FIRACODE_VERSION="3.1"
IOSEVKA_VERSION="latest"
IOSEVKA_VARIANT="FixedSS05" # Use fixed version of Fira Mono style variant

ASSETS_DIR=$(realpath "$SCRIPT_DIR/../assets")
OUTPUT_DIR=$(realpath "$SCRIPT_DIR/../build")
SRC_DIR=$(realpath "$SCRIPT_DIR/../src")

prerequisite() {
  dybatpho::require 'grep'
  dybatpho::require 'unzip'
  dybatpho::require 'fontforge'
  dybatpho::require 'docker'
}

download_iosevka() {
  if dybatpho::is file "$ASSETS_DIR/IosevkaFixedSS05-Regular.ttf"; then
    dybatpho::info "Already have Iosevka font"
    return
  fi
  if [ "${IOSEVKA_VERSION}" == "latest" ]; then
    local temp_file_1=$(mktemp)
    dybatpho::cleanup_file_on_exit "$temp_file_1"
    dybatpho::curl_do https://api.github.com/repos/be5invis/Iosevka/releases/latest "$temp_file_1"
    IOSEVKA_VERSION=$(grep -Po "tag_name\": \"(\K.*)(?=\",)" "$temp_file_1")
  fi
  dybatpho::notice "Downloading Iosevka font version: ${IOSEVKA_VERSION}"
  local temp_file_2=$(mktemp)
  dybatpho::cleanup_file_on_exit "$temp_file_2"
  dybatpho::curl_download \
    "https://github.com/be5invis/Iosevka/releases/download/${IOSEVKA_VERSION}/PkgTTF-Iosevka${IOSEVKA_VARIANT}-${IOSEVKA_VERSION:1}.zip" \
    "$temp_file_2"
  unzip -qqo "$temp_file_2" -d "${ASSETS_DIR}"
  dybatpho::success "Downloaded Iosevka"
}

download_firacode() {
  dybatpho::notice "Downloading FiraCode font version: ${FIRACODE_VERSION}"
  local fira_style_names=("Regular" "Bold")
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

patch_nerd() {
  dybatpho::notice "Patching Nerd Font"
  local style_names=("Regular" "Italic" "Bold" "BoldItalic")
  local font_suffixes=("" " Italic" " Bold" " Bold Italic")
  local style_count=0
  for style_name in "${style_names[@]}"; do
    local input_filename="iosevka-dynamo-$(dybatpho::lower "$style_name").ttf"
    local patched_filename="IosevkaDynamoNerd-${style_name}.ttf"
    local output_filename="iosevka-dynamo-nerd-$(dybatpho::lower "$style_name").ttf"
    docker run --rm \
      -v "$OUTPUT_DIR/${input_filename}":/in/iosevka-dynamo.ttf \
      -v "$OUTPUT_DIR":/out \
      nerdfonts/patcher \
      --name "'Iosevka Dynamo Nerd${font_suffixes[$style_count]}'" \
      --mono --fontawesome --codicons --material --octicons --careful
    ((style_count += 1))
    sudo mv "${OUTPUT_DIR}/${patched_filename}" \
      "${OUTPUT_DIR}/${output_filename}"
    sudo chown "$USER" "${OUTPUT_DIR}/${output_filename}"
  done
}

main() {
  download_iosevka
  download_firacode

  local style_names=("Regular" "Italic" "Oblique" "Bold" "BoldItalic" "BoldOblique")
  local style_count=0
  for style_name in "${style_names[@]}"; do
    [[ "$style_name" =~ Bold* ]] && fira_style="Bold" || fira_style="Regular"
    local suffix="${style_names[$style_count]}"
    dybatpho::notice "Make font ${FONT_FAMILY_NAME} ${suffix}"
    "${SRC_DIR}/main.py" \
      "${ASSETS_DIR}/Iosevka${IOSEVKA_VARIANT}-${style_name}.ttf" \
      "$(realpath "${ASSETS_DIR}/FiraCode-${fira_style}.otf")" \
      -n "$FONT_FAMILY_NAME" \
      -s "$suffix" -d \
      -v "${FONT_FAMILY_VERSION}" \
      -D "$OUTPUT_DIR"
    ((style_count += 1))
  done
  dybatpho::success "Created font $FONT_FAMILY_NAME"

  patch_nerd
  dybatpho::success "Patched Nerd Font"
}

prerequisite
main
