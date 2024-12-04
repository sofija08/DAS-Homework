package com.example.project1.data;

import com.example.project1.data.pipeline.Pipe;
import com.example.project1.data.pipeline.impl.FilterCorporate;
import com.example.project1.data.pipeline.impl.FilterCorporateData;
import com.example.project1.data.pipeline.impl.FilterReAddCorporateData;
import com.example.project1.model.CorporateEntity;
import com.example.project1.repository.CorporateRepository;
import com.example.project1.repository.TradeHistoryRepository;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.text.ParseException;
import java.util.List;

@Component
@RequiredArgsConstructor
public class Initializr {

    private final CorporateRepository corporateRepository;
    private final TradeHistoryRepository tradeHistoryRepository;

    @PostConstruct
    private void initializeData() throws IOException, ParseException {
        long startTime = System.nanoTime();

        Pipe<List<CorporateEntity>> pipe = new Pipe<>();
        pipe.addFilter(new FilterCorporate(corporateRepository));
        pipe.addFilter(new FilterCorporateData(corporateRepository, tradeHistoryRepository));
        pipe.addFilter(new FilterReAddCorporateData(corporateRepository, tradeHistoryRepository));
        pipe.runFilter(null);

        long endTime = System.nanoTime();
        long durationInMillis = (endTime - startTime) / 1_000_000;

        long hours = durationInMillis / 3_600_000;
        long minutes = (durationInMillis % 3_600_000) / 60_000;
        long seconds = (durationInMillis % 60_000) / 1_000;

        System.out.printf("Total time for all filters to complete: %02d hours, %02d minutes, %02d seconds%n", hours, minutes, seconds);
    }

}
