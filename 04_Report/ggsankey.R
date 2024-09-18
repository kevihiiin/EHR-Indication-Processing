library(data.table)
library(ggplot2)
library(ggsankey)
library(viridis)


ID_Indication_Label_SourceByDiagCode <- fread("/Users/guqingze/Library/CloudStorage/OneDrive-Nexus365/R Projects/ID_Indication_Label_SourceByDiagCode.csv")
nrow(ID_Indication_Label_SourceByDiagCode[, .SD[1], by = ClusterID])
nrow(ID_Indication_Label_SourceByDiagCode[, .SD[1], by = EpisodeID])
ID_Indication_Label_SourceByDiagCode[, .N, by = TrueLabel][order(-N)]

UnspecificDiagCode_to_label <- ID_Indication_Label_SourceByDiagCode[SourceByDiagCode == "Unspecific" & TrueLabel != "Unspecific"]
UnspecificDiagCode_to_label[, .N, by = TrueLabel][order(-N)]


ID_Indication_Label_SourceByDiagCode$TrueLabel <- factor(ID_Indication_Label_SourceByDiagCode$TrueLabel,
                                                         levels = c("Unspecific", "Respiratory", "Urinary", "Multiple sources", "Abdominal", "Skin, soft tissue", "Orthopedic", "ENT", "CNS", "Other"))
ID_Indication_Label_SourceByDiagCode$SourceByDiagCode <- factor(ID_Indication_Label_SourceByDiagCode$SourceByDiagCode,
                                                                levels = c("Unspecific", "Respiratory", "Urinary", "Multiple sources", "Abdominal", "Skin, soft tissue, orthopedic", "CNS", "Other"))

# setnames(ID_Indication_Label_SourceByDiagCode, c("TrueLabel", "SourceByDiagCode"), c("Ground-truth Labels", "Diagnose Codes"))

Label_SourceByDiagCode_long <- make_long(ID_Indication_Label_SourceByDiagCode, TrueLabel, SourceByDiagCode)

setDT(Label_SourceByDiagCode_long)

Label_SourceByDiagCode_long$node <- factor(Label_SourceByDiagCode_long$node,
                                           levels = c("Other", "CNS", "ENT", "Orthopedic", "Skin, soft tissue", "Skin, soft tissue, orthopedic", "Multiple sources", "Abdominal", "Urinary", "Respiratory", "Unspecific"))
Label_SourceByDiagCode_long$next_node <- factor(Label_SourceByDiagCode_long$next_node,
                                           levels = c("Other", "CNS", "ENT", "Orthopedic", "Skin, soft tissue", "Skin, soft tissue, orthopedic", "Multiple sources", "Abdominal", "Urinary", "Respiratory", "Unspecific"))

color_manual = c("Unspecific" = "#BC3C29", "Respiratory" = "#0072B5", "Urinary" = "#E18727", "Abdominal" = "#20854E", "Skin, soft tissue, orthopedic" = "#7876B1", "Skin, soft tissue" = "#7876B1", "Orthopedic" ="#5F559B",
                 "ENT" = "#6F99AD", "CNS" = "#FFDC91", "Multiple sources" = "#EE4C97", "Other" = "#7E6148")

p_sankey_source <- 
        ggplot(Label_SourceByDiagCode_long, 
               aes(x = x, next_x = next_x, node = node, next_node = next_node, 
                   fill = factor(node),
                   label = node)) +
        geom_sankey(flow.alpha = .6) +
        geom_sankey_label(size = 3, color = "black", fill = "white", alpha = 0.6) +
        scale_fill_manual(values = color_manual) +
        theme_sankey(base_size = 18) +
        labs(x = NULL) +
        theme(legend.position = "none",
              plot.title = element_text(hjust = .5)) +
        ggtitle("Sources of Infection")

p_sankey_source

ggsave(filename = "sankey_source.pdf", device = "pdf",
       plot = p_sankey_source,
       path = "/Users/guqingze/Library/CloudStorage/OneDrive-Nexus365/R Projects/",
       width = 14, height = 10,
       dpi = 320)
