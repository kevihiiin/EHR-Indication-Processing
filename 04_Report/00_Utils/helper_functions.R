# --------------------------------------
# Shared paths and functions
# --------------------------------------

# --- Paths
base_data_path <- "../../00_Data/"

# Final data path
publication_ready_path <- paste(base_data_path, "publication_ready", sep = "/")

# Look up table path
lut_path <- paste0(base_data_path, "LUTs/")

# Plot's path
plot_path <- paste0(publication_ready_path, "/plots/")

# --- General Settings
# Max decimal places to round to
round_decimals = 2

# --- Helper Functions
clean_category_names <- function(input_df){
  old_names <- colnames(input_df)
  
  # Replace dashes with spaces and capitalize
  new_names <- old_names %>%
    gsub("_", " ", .) %>%  # replace underscores with spaces
    tools::toTitleCase()   # capitalize first letter of each word
  
  # Handle specific cases [gsub("old", "new")]
  new_names <- new_names %>%
    gsub("Ent", "ENT", .) %>%
    gsub("Skin Soft Tissue", "Skin & Soft Tissue", .)
  
  # Assign the new names back to the dataframe
  colnames(input_df) <- new_names
  
  return(input_df)
}

source_categories <-
  c(
    "Urinary",
    "Respiratory",
    "Abdominal",
    "Neurological",
    "Skin & Soft Tissue",
    "ENT",
    "Orthopaedic",
    "Other Specific",
    "No Specific Source",
    "Prophylaxis",
    # "Uncertainty",
    "Not Informative"
  )

# --- Style
theme_set(theme_light())
