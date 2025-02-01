package com.example.examplemod;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import com.mojang.logging.LogUtils;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.DeferredHolder;

@Mod(ExampleMod.MODID)
public class ExampleMod {
    public static final String MODID = "examplemod";
    private static final Logger LOGGER = LogUtils.getLogger();

    // Rejestry dla bloków, przedmiotów i kart kreatywnych
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(MODID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MODID);
    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);

    // Lista dynamicznych nazw bloków – np. Twój skrypt w Pythonie wstawia tutaj "abcde"
    public static final List<String> DYNAMIC_BLOCK_NAMES = List.of(
            "test1"
    );

    // Mapy przechowujące zarejestrowane dynamiczne bloki oraz odpowiadające im BlockItemy
    public static final Map<String, DeferredBlock<Block>> DYNAMIC_BLOCKS = new HashMap<>();
    public static final Map<String, DeferredItem<BlockItem>> DYNAMIC_BLOCK_ITEMS = new HashMap<>();

    // Rejestrujemy dynamiczne bloki i odpowiadające im BlockItemy
    static {
        for (String blockName : DYNAMIC_BLOCK_NAMES) {
            DeferredBlock<Block> block = BLOCKS.registerSimpleBlock(
                    blockName,
                    BlockBehaviour.Properties.of().mapColor(MapColor.STONE)
            );
            DYNAMIC_BLOCKS.put(blockName, block);
            DYNAMIC_BLOCK_ITEMS.put(blockName, ITEMS.registerSimpleBlockItem(blockName, block));
        }
    }

    // Rejestrujemy dedykowaną kartę kreatywną, na której wyświetlamy dynamiczne bloki
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> MOD_TAB = CREATIVE_MODE_TABS.register("mod_tab", () ->
            CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.examplemod"))
                    .withTabsBefore(CreativeModeTabs.BUILDING_BLOCKS)
                    // Używamy pierwszego dynamicznego bloku jako ikony (zakładamy, że lista nie jest pusta)
                    .icon(() -> DYNAMIC_BLOCK_ITEMS.get(DYNAMIC_BLOCK_NAMES.get(0)).get().getDefaultInstance())
                    .displayItems((parameters, output) -> {
                        for (DeferredItem<BlockItem> item : DYNAMIC_BLOCK_ITEMS.values()) {
                            output.accept(item.get());
                        }
                    }).build()
    );

    public ExampleMod(IEventBus modEventBus, ModContainer modContainer) {
        // Rejestracja Deferred Register – dzięki nim rejestracja nastąpi we właściwym momencie
        BLOCKS.register(modEventBus);
        ITEMS.register(modEventBus);
        CREATIVE_MODE_TABS.register(modEventBus);

        // Rejestrujemy metodę commonSetup na mod busie
        modEventBus.addListener(this::commonSetup);
        // Uwaga: nie rejestrujemy 'this' na NeoForge.EVENT_BUS, aby nie trafić na błędy związane z IModBusEvent.
    }

    private void commonSetup(FMLCommonSetupEvent event) {
        LOGGER.info("Common setup complete for mod {}", MODID);
    }

    // Statyczny event subscriber na MOD busie do obsługi zdarzenia budowania zawartości kreatywnej karty BUILDING_BLOCKS
    @EventBusSubscriber(modid = MODID, bus = EventBusSubscriber.Bus.MOD)
    public static class ModEvents {
        @SubscribeEvent
        public static void onBuildCreative(BuildCreativeModeTabContentsEvent event) {
            if (event.getTabKey() == CreativeModeTabs.BUILDING_BLOCKS) {
                for (DeferredItem<BlockItem> item : DYNAMIC_BLOCK_ITEMS.values()) {
                    event.accept(item.get());
                }
            }
        }
    }

    // Statyczny event subscriber na MOD busie dla zdarzeń klienta
    @EventBusSubscriber(modid = MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
    public static class ClientEvents {
        @SubscribeEvent
        public static void onClientSetup(FMLClientSetupEvent event) {
            LOGGER.info("Client setup complete for mod {}", MODID);
        }
    }
}
