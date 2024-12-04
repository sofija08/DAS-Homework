package com.example.project1.data.pipeline.impl;

import com.example.project1.data.pipeline.Filter;
import com.example.project1.model.CorporateEntity;
import com.example.project1.repository.CorporateRepository;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.List;

public class FilterCorporate implements Filter<List<CorporateEntity>> {

    private final CorporateRepository corporateRepository;

    public FilterCorporate(CorporateRepository corporateRepository) {
        this.corporateRepository = corporateRepository;
    }

    private static final String STOCK_MARKET_URL = "https://www.mse.mk/mk/stats/symbolhistory/kmb";

    @Override
    public List<CorporateEntity> execute(List<CorporateEntity> input) throws IOException {
        Document document = Jsoup.connect(STOCK_MARKET_URL).get();
        Element selectMenu = document.select("select#Code").first();

        if (selectMenu != null) {
            Elements options = selectMenu.select("option");
            for (Element option : options) {
                String code = option.attr("value");
                if (!code.isEmpty() && code.matches("^[a-zA-Z]+$")) {
                    if (corporateRepository.findByCompanyCode(code).isEmpty()) {
                        corporateRepository.save(new CorporateEntity(code));
                    }
                }
            }
        }

        return corporateRepository.findAll();
    }
}
